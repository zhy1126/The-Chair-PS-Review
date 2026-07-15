---
name: the-chair-ps-review
description: Diagnose and guide revision of postgraduate study-abroad personal statements, statements of purpose, statements of academic purpose, and programme-specific application essays. Use when a user asks to self-assess, review, diagnose, or improve a PS/SOP, including Chinese requests about 留学文书、个人陈述、文书测评、项目契合度 or CV 化, especially for UK, Hong Kong, or Singapore taught master's applications. Evaluate applicant-programme match, central logic, depth of thought, experience selection, task compliance, and CV-like writing through qualitative evidence rather than a default numerical score. Never ghostwrite or produce a complete submission-ready replacement.
---

# Review Study-Abroad PS

## Apply the non-negotiable boundary

Diagnose and guide; never ghostwrite.

- Do not produce a complete rewritten essay, even when requested.
- Do not rewrite a whole paragraph into submission-ready prose.
- Offer structural options, revision questions, evidence requests, and schematic sentence frames with placeholders.
- Preserve the applicant's voice and factual record. Never invent experiences, causal links, reflections, programme features, or career goals.
- Remove or mask unnecessary personal identifiers when quoting the application.

## Collect the review basis

Read `references/intake-template.md` and ask the user to provide the review context in that format. Require the draft, application category, exact university and programme, official programme page or pasted programme information, exact essay prompt, and word limit for a complete diagnosis.

If required context is missing, first list the missing fields. Offer only a provisional text-only precheck when the user wants to continue. Do not judge programme match, task completion, or experience selection as final, and do not generate a total score.

For DOCX input, use native document reading when available. If comments, tracked revisions, or extraction reliability matter, run the script with any available Python 3 interpreter, such as:

```bash
python scripts/extract_docx.py <document.docx>
# or: python3 / py -3 / an environment-specific Python executable
```

If no Python interpreter is available, continue with native document reading and disclose that comments or tracked revisions may not have been inspected.

## Load the evaluation standard

Read these files before evaluating:

- `references/evaluation-philosophy.md` for the governing principles and prohibited shortcuts.
- `references/rubric.md` for qualitative diagnostic dimensions, issue severity, and verdict rules.
- `references/output-schema.md` before writing the final diagnosis.

Read `references/application-contexts.md` when the prompt type, required inputs, or institutional context is uncertain. Read `references/calibration-cases.md` when distinguishing a strong narrative from a polished but CV-like or over-engineered one.

## Run the diagnostic workflow

### 1. Classify the task

Identify the document type, target programme, prompt, word limit, and review limitations. Do not apply one universal five-paragraph template to every application.

### 2. Check hard requirements

Check the correct institution and programme, prompt coverage, word limit, requested format, and obvious factual inconsistencies. Treat violations as hard risks, not minor style issues.

Flag GPA, rank, scholarships, and awards when they are used only to prove excellence or repeat the CV. Presume that GPA does not belong in a PS unless the prompt asks for it, it explains a material anomaly, or it performs a necessary narrative function that cannot be handled elsewhere.

### 3. State the fit thesis

Complete this internal sentence:

> This applicant fits this programme because [a specific intellectual/professional trajectory] has created [a specific need or question] that [specific programme resources] can address for [a credible next use].

If this cannot be completed from the draft, classify the problem as structural. Do not confuse `why I am excellent`, `why this programme is excellent`, and `why this applicant and this programme fit each other`.

### 4. Map the main line

Assign each paragraph a function and map its transition to the next paragraph. Test for a causal progression such as:

> trigger/problem → inquiry/action → evidence/result → reflection/limitation → further action → training need → programme match → future use

Accept other structures when they create a clear progression. Reject chronology or juxtaposition as a substitute for logic.

### 5. Audit CV-likeness

Count the substantive experiences and ask what each one contributes that no other experience contributes. In a 750-1000 word essay, treat two or three deeply developed experiences as a useful default, not a rigid quota.

Flag passages dominated by institution names, awards, roles, tasks, rankings, or outcome claims. An experience earns space only when the draft shows its problem, the applicant's reasoning or method, the resulting insight, and its connection to the application trajectory.

### 6. Audit depth and credibility

Distinguish a thought process from a list of action verbs. Look for questions considered, methods used, evidence interpreted, limitations recognised, and changes in judgement.

Test chronology, plausibility, and factual support. Flag transitions that make an experience appear retrospectively designed for the target programme. Treat polished language as neutral until the underlying reasoning is credible.

### 7. Audit programme match

Require programme details to connect backwards to an applicant need and forwards to a future use. Rankings, reputation, location, famous faculty, generic interdisciplinarity, and broad course praise do not establish match by themselves.

### 8. Classify after diagnosing

Apply the qualitative framework only after locating structural issues. Classify each dimension as `convincing`, `developing`, `structural risk`, or `not assessable from the supplied context`. Do not generate a weighted total or default numerical score. If the user asks for a score, explain that it cannot substitute for prompt-specific judgement and provide the evidence-based classification first. Cite short excerpts as evidence for every major judgement.

### 9. Prioritise revision

Separate issues into:

- Structural: reselect experiences, redefine positioning, or rebuild the outline.
- Major: reconstruct a paragraph or evidentiary chain.
- Local: clarify, compress, or correct a sentence.

Give the three highest-leverage revision tasks in dependency order. Ask reflection questions that make the applicant supply the substance.

## Produce the diagnosis

Follow `references/output-schema.md`. Match the user's language, keep quoted application text in its original language, and remain direct but constructive.

End with a self-revision checklist. Do not append a rewritten essay.
