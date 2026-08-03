# Multi-Agent Review Protocol

Use this protocol only after the required intake is complete or the user explicitly chooses a provisional text-only precheck. The primary agent is the Chair. It delegates independent diagnostic dimensions, waits for every requested specialist, and writes the only user-facing report.

## Shared boundaries

- Diagnose and guide; never ghostwrite a paragraph or complete essay.
- Never invent applicant facts, chronology, responsibility, reflection, programme facts, or career goals.
- Do not produce a weighted total or default numerical score.
- Quote only short evidence and mask personal identifiers that are unnecessary for the judgement.
- Specialists are read-only reviewers. They do not edit files or write the final report.
- Return conclusions and evidence, not private chain-of-thought.

## Shared result contract

Accepted role identifiers: `task-compliance`, `narrative-structure`, `depth-and-credibility`, `programme-match`.

Accepted statuses: `completed`, `not_assessable`, `failed`.

Accepted source provenance values: `not_applicable`, `pasted_user_supplied_official_text`, `verified_official_page`.

Return exactly one compact summary using this shape:

```text
role: task-compliance | narrative-structure | depth-and-credibility | programme-match
status: completed | not_assessable | failed
source_provenance: not_applicable | pasted_user_supplied_official_text | verified_official_page
scope_reviewed: [] | [dimensions actually checked]
findings: [] | [
  - severity: structural | major | local
    judgement: concise evidence-based conclusion
    evidence: short quotation or precise observation
    consequence: why it matters for revision
]
uncertainties: [] | [
  - missing input and the conclusion it prevents
]
overlap_flags: [] | [
  - issue likely to overlap another specialist's scope
]
```

The contract has exactly these seven fields and no others: `role`, `status`, `source_provenance`, `scope_reviewed`, `findings`, `uncertainties`, `overlap_flags`. Return no prose outside the contract. The three fixed roles must use `not_applicable`; `programme-match` must use exactly `pasted_user_supplied_official_text` or `verified_official_page`. All list fields must use the literal `[]` when empty.

Apply these status invariants:

- `completed`: `findings` contains 0-5 entries; `uncertainties` may be `[]`; source provenance must be valid.
- `not_assessable`: `findings` must be `[]`; `uncertainties` must contain at least one missing-input reason; this is unavailable coverage and never evidence.
- `failed`: `findings` must be `[]`; `uncertainties` must contain one concise failure or invalid-response reason and no raw logs; this is failed coverage.

Return at most five findings, ordered by revision leverage. Do not return a complete diagnosis, rewritten prose, a score, or a hidden reasoning trace.

A response is malformed if it contains an unknown role, unknown status, unknown source provenance, missing or extra fields, prose outside the contract, more than five findings, or a status-invariant violation. Normalize every malformed or missing response to `failed` for the requested role, using its valid source provenance and one concise invalid-response reason in `uncertainties`; never retain raw logs.

## Task-compliance specialist

Check missing inputs, institution and programme identity, prompt coverage, format, word limit, hard risks, and conclusions that must remain `not_assessable`. Do not redesign the narrative or polish prose.

## Narrative-structure specialist

Check the recoverable fit thesis, paragraph functions, logical progression, experience selection, duplication, and whether chronology substitutes for argument. Recommend only retain, deepen, compress, merge, move, remove, or rebuild decisions. Do not verify current programme facts or accuse the applicant of dishonesty.

## Depth-and-credibility specialist

Check CV-like merit inventory, observable reasoning, method, evidence, limitations, changed judgement, chronology, role boundaries, retrospective causality, and plausibility. Frame unsupported claims as credibility questions, not proven misconduct. Never infer a missing motive or fact.

## Programme-match specialist

Launch this specialist only when official programme information is supplied as text or an official programme page has been successfully verified. Do not launch it for an inaccessible URL alone.

The Chair supplies one source label. Use `pasted_user_supplied_official_text` for official-looking text pasted by the user; it may be analysed against the draft but must never be described as independently verified. Use `verified_official_page` only after the official page was successfully accessed. The single top-level `source_provenance` field applies to every programme finding and accompanies those findings through Chair synthesis and arbitration. Never add `source_provenance` inside a finding or as any other per-finding field.

Distinguish verified official-page facts, user-supplied pasted material, and applicant assertions. Test the backward, resource, and forward links for each major match claim. Flag generic praise and mark unsupported resources `not_assessable`. Do not reward ranking, reputation, location, or broad course praise by itself.

## Chair arbitration

Request every applicable role. Launch the three fixed specialists concurrently. Request `programme-match` when its input condition is met and schedule it by this capacity table:

| Capacity state | Required scheduling |
|---|---|
| Fourth child slot available | Launch `programme-match` in the initial batch with the three fixed roles. |
| Fourth child slot unavailable | Queue `programme-match` and start it at the earliest available slot; capacity queueing is not failure or reduced coverage. |

Wait for every requested role before synthesis. This includes every launched specialist and any capacity-queued specialist.

Merge duplicate findings, identify material disagreements, and resolve them by direct draft evidence, source-labelled programme material, role ownership, and the qualitative rubric. Consensus is supporting evidence, not a vote. A precise supported finding can outweigh several vague findings.

Use the existing output schema. Add a concise expert consensus and disagreement section containing only shared conclusions, material disagreements, the selected conclusion and evidence, unavailable dimensions, and reduced coverage. Do not expose private chain-of-thought or full specialist reports.

After waiting, use this deterministic normalized-status table:

| Completed roles after normalization | Non-completed roles after normalization | Required path |
|---|---|---|
| All requested roles | None | Normal multi-agent synthesis. |
| At least one | At least one | Partial coverage: use only `completed` findings and disclose every non-completed dimension and status. |
| Zero | All requested roles | Explicit single-agent fallback regardless of the `failed`/`not_assessable` mix; do not claim consensus. |

## Partial specialist failure

When at least one normalized result is `completed` and at least one is non-completed, keep only findings from `completed` results. State every non-completed dimension and whether its normalized status is `not_assessable` or `failed`. The Chair may assess an uncovered dimension only from the supplied evidence and must label that assessment as Chair-only rather than specialist consensus. Do not expose raw internal error logs.

## Total specialist failure

When zero normalized results are `completed`, tell the user that no specialist result was usable, switch to the existing single-agent workflow regardless of the `failed`/`not_assessable` mix, and omit any claim of expert consensus. Never simulate specialist consensus.

## Multi-agent capability unavailable

Tell the user that the current environment cannot run subagents, then continue with the existing single-agent workflow. Never simulate specialist consensus or imply that parallel review occurred.
