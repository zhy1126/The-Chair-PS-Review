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
- Read `references/multi-agent-protocol.md` for specialist roles, parallel dispatch, result contracts, arbitration, privacy, and fallback behaviour.

Read `references/application-contexts.md` when the prompt type, required inputs, or institutional context is uncertain. Read `references/calibration-cases.md` when distinguishing a strong narrative from a polished but CV-like or over-engineered one.

## Orchestrate the multi-agent diagnosis

The primary agent remains the Chair. Delegate only after the required intake is complete or the user explicitly accepts a provisional text-only precheck.

Prepare the smallest sufficient shared context: application type, document type, institution and programme, exact prompt, word limit, applicant background, draft, verified or pasted official programme information, and known limitations. Remove or mask identifiers that are unnecessary for review. Before launching `programme-match`, label its programme source as `pasted_user_supplied_official_text`, `verified_official_page`, or none. User-pasted official-looking text may be analysed, but it must never be called independently verified. Use `verified_official_page` only after an official page was successfully accessed.

Then prepare a separately minimized packet for each specialist: task-compliance gets prompt, limits, institution, programme, and draft but no irrelevant background; narrative gets draft plus only trajectory/background needed to understand progression; depth/credibility gets draft plus only chronology/role context needed; programme-match gets only draft match claims, training needs, source-labelled verified/pasted official programme information, and its `source_provenance`. Do not send official programme material to roles that do not need it.

When subagent tools are available:

1. Request every applicable specialist role using the bounded instructions and result contract in `references/multi-agent-protocol.md`.
2. Always request `task-compliance`, `narrative-structure`, and `depth-and-credibility`. Launch the three fixed roles concurrently.
3. Request `programme-match` only when official programme information was pasted by the user or an official page was successfully verified. Do not launch the programme-match specialist for an inaccessible URL alone. Schedule the requested conditional role by this table:

| Capacity state | Required scheduling |
|---|---|
| Fourth child slot available | Launch `programme-match` in the initial batch with the three fixed roles. |
| Fourth child slot unavailable | Queue `programme-match` and start it at the earliest available slot; capacity queueing is not failure or reduced coverage. |

4. Capacity queueing is not failure or reduced coverage. Wait for every requested specialist before synthesising the diagnosis, including any queued role.
5. Validate every returned summary against the shared result contract before synthesis: accept only known roles, valid statuses, required compact fields, and at most five findings. Retain only contract fields. Treat missing, malformed, or overlong responses as failed. Record valid `not_assessable` as unavailable coverage and never as evidence. Determine partial or total failure from normalized statuses.
6. Treat specialist conclusions as evidence, not votes. Resolve overlap and conflict with the draft, source-labelled programme material, role ownership, and `references/rubric.md`. The programme specialist and Chair must retain `source_provenance` through final programme claims and arbitration.

Normalize against these exact enums and fields. Accepted role identifiers: `task-compliance`, `narrative-structure`, `depth-and-credibility`, `programme-match`. Accepted statuses: `completed`, `not_assessable`, `failed`. Accepted source provenance values: `not_applicable`, `pasted_user_supplied_official_text`, `verified_official_page`. A summary contains exactly these seven fields: `role`, `status`, `source_provenance`, `scope_reviewed`, `findings`, `uncertainties`, `overlap_flags`; retain no extra prose or fields. The three fixed roles require `not_applicable`; `programme-match` requires one of the two programme-source values. All list fields use the literal `[]` when empty.

Apply these invariants: `completed` permits 0-5 findings and empty uncertainties with valid provenance; `not_assessable` requires `findings: []` and at least one missing-input reason in uncertainties and is unavailable coverage, never evidence; `failed` requires `findings: []` and one concise failure or invalid-response reason in uncertainties, with no raw logs, and is failed coverage. Unknown role, status, or provenance; missing or extra fields; prose outside the contract; more than five findings; and any status-invariant violation are malformed. Normalize every malformed or missing response to `failed` for the requested role with valid provenance and one concise reason.

After waiting, apply this deterministic table:

| Completed roles after normalization | Non-completed roles after normalization | Required path |
|---|---|---|
| All requested roles | None | Normal multi-agent synthesis. |
| At least one | At least one | Partial coverage: use only `completed` findings and disclose every non-completed dimension and status. |
| Zero | All requested roles | Explicit single-agent fallback regardless of the `failed`/`not_assessable` mix; do not claim consensus. |

If subagent tools are disabled or unavailable, tell the user before falling back to the existing single-agent diagnostic workflow below. If zero normalized results are `completed`, use the same explicit fallback even when the non-completed results mix `failed` and `not_assessable`. Never claim expert consensus after a full fallback. If at least one normalized result is `completed` and at least one is non-completed, preserve only the completed findings and disclose every non-completed dimension and status in the final transparency section.

Do not expose private chain-of-thought or append full specialist reports. Never carry full specialist reports or private reasoning into Chair synthesis. The Chair writes one report only.

## Apply the diagnostic and synthesis checklist

Use the following steps as the shared diagnostic standard and as the Chair's synthesis checklist. Do not perform a duplicate full review before launching specialists.

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

Include a self-revision checklist before the final expert consensus and disagreement section. Do not append a rewritten essay.

