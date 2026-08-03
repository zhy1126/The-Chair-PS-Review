from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skill" / "the-chair-ps-review"
PROTOCOL = SKILL_DIR / "references" / "multi-agent-protocol.md"
SKILL = SKILL_DIR / "SKILL.md"
OUTPUT_SCHEMA = SKILL_DIR / "references" / "output-schema.md"
README = ROOT / "README.md"
OPENAI_YAML = SKILL_DIR / "agents" / "openai.yaml"
MANUAL_SCENARIOS = ROOT / "tests" / "manual-scenarios.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def section(document: str, heading: str) -> str:
    start = document.index(heading)
    end = document.find("\n## ", start + len(heading))
    return document[start:] if end == -1 else document[start:end]


class MultiAgentProtocolTests(unittest.TestCase):
    def test_protocol_defines_bounded_specialists_and_result_contract(self) -> None:
        self.assertTrue(PROTOCOL.exists(), "multi-agent protocol reference is missing")
        protocol = read(PROTOCOL)
        for heading in (
            "## Task-compliance specialist",
            "## Narrative-structure specialist",
            "## Depth-and-credibility specialist",
            "## Programme-match specialist",
            "## Chair arbitration",
        ):
            self.assertIn(heading, protocol)
        for field in (
            "role:",
            "status: completed | not_assessable | failed",
            "scope_reviewed:",
            "findings:",
            "uncertainties:",
            "overlap_flags:",
        ):
            self.assertIn(field, protocol)
        self.assertIn("Return at most five findings", protocol)

    def test_protocol_preserves_primary_safety_boundaries(self) -> None:
        protocol = read(PROTOCOL)
        for boundary in (
            "never ghostwrite a paragraph or complete essay",
            "Never invent applicant facts",
            "Do not produce a weighted total or default numerical score",
            "mask personal identifiers that are unnecessary for the judgement",
            "Specialists are read-only reviewers",
            "not private chain-of-thought",
        ):
            self.assertIn(boundary, protocol)

    def test_chair_orchestrates_and_arbitrates_from_evidence_not_votes(self) -> None:
        protocol = read(PROTOCOL)
        chair = section(protocol, "## Chair arbitration")
        self.assertIn("The primary agent is the Chair", protocol)
        self.assertIn("writes the only user-facing report", protocol)
        self.assertIn("Launch the three fixed specialists in parallel", chair)
        self.assertIn("Wait for every launched specialist before synthesis", chair)
        self.assertIn(
            "resolve them by direct draft evidence, verified official facts, role ownership, and the qualitative rubric",
            chair,
        )
        self.assertIn("Consensus is supporting evidence, not a vote", chair)

    def test_protocol_makes_programme_review_conditional_and_defines_fallbacks(self) -> None:
        protocol = read(PROTOCOL)
        self.assertIn("Do not launch it for an inaccessible URL alone", protocol)
        self.assertIn("## Partial specialist failure", protocol)
        total_failure = section(protocol, "## Total specialist failure")
        unavailable = section(protocol, "## Multi-agent capability unavailable")
        self.assertIn("Never simulate specialist consensus", total_failure)
        self.assertIn("Never simulate specialist consensus", unavailable)


if __name__ == "__main__":
    unittest.main()
