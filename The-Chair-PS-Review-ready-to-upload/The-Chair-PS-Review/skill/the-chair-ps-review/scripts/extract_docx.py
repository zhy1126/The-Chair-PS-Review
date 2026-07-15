#!/usr/bin/env python3
"""Extract visible text, comments, and revision counts from DOCX files."""

from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def _read_xml(archive: zipfile.ZipFile, name: str) -> ET.Element | None:
    try:
        return ET.fromstring(archive.read(name))
    except KeyError:
        return None


def _paragraph_text(paragraph: ET.Element) -> str:
    parts: list[str] = []

    def visit(node: ET.Element, deleted: bool = False) -> None:
        is_deleted = deleted or node.tag == W + "del"
        if node.tag == W + "t" and not is_deleted:
            parts.append(node.text or "")
        elif node.tag == W + "tab" and not is_deleted:
            parts.append("\t")
        elif node.tag in {W + "br", W + "cr"} and not is_deleted:
            parts.append("\n")
        for child in node:
            visit(child, is_deleted)

    visit(paragraph)
    return "".join(parts).strip()


def _all_paragraphs(root: ET.Element | None) -> list[str]:
    if root is None:
        return []
    return [text for p in root.iter(W + "p") if (text := _paragraph_text(p))]


def extract_docx(path: Path) -> dict:
    with zipfile.ZipFile(path) as archive:
        document = _read_xml(archive, "word/document.xml")
        if document is None:
            raise ValueError("word/document.xml is missing")

        paragraphs = _all_paragraphs(document)
        text = "\n".join(paragraphs)
        headers: dict[str, str] = {}
        for name in archive.namelist():
            if re.fullmatch(r"word/(header|footer)\d+\.xml", name):
                entry_text = "\n".join(_all_paragraphs(_read_xml(archive, name)))
                if entry_text:
                    headers[name] = entry_text

        comments_root = _read_xml(archive, "word/comments.xml")
        comments: list[dict] = []
        if comments_root is not None:
            for comment in comments_root.iter(W + "comment"):
                comment_text = "\n".join(_all_paragraphs(comment))
                comments.append(
                    {
                        "id": comment.attrib.get(W + "id", ""),
                        "author": comment.attrib.get(W + "author", ""),
                        "date": comment.attrib.get(W + "date", ""),
                        "text": comment_text,
                    }
                )

        return {
            "path": str(path),
            "word_count": len(re.findall(r"\b[\w'-]+\b", text, flags=re.UNICODE)),
            "paragraph_count": len(paragraphs),
            "insertions": sum(1 for _ in document.iter(W + "ins")),
            "deletions": sum(1 for _ in document.iter(W + "del")),
            "comments": comments,
            "headers_and_footers": headers,
            "text": text,
        }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("documents", nargs="+", type=Path)
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()

    results = []
    for document in args.documents:
        try:
            results.append(extract_docx(document))
        except Exception as exc:  # report per file without hiding other results
            results.append({"path": str(document), "error": str(exc)})

    payload = results[0] if len(results) == 1 else results
    json.dump(
        payload,
        sys.stdout,
        ensure_ascii=False,
        indent=2 if args.pretty else None,
    )
    sys.stdout.write("\n")
    return 1 if any("error" in result for result in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
