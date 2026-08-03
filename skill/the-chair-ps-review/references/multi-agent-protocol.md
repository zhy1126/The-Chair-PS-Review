# Multi-Agent Review Protocol

Use this protocol only after the required intake is complete or the user explicitly chooses a provisional text-only precheck. The primary agent is the Chair. It delegates independent diagnostic dimensions, waits for every launched specialist, and writes the only user-facing report.

## Shared boundaries

- Diagnose and guide; never ghostwrite a paragraph or complete essay.
- Never invent applicant facts, chronology, responsibility, reflection, programme facts, or career goals.
- Do not produce a weighted total or default numerical score.
- Quote only short evidence and mask personal identifiers that are unnecessary for the judgement.
- Specialists are read-only reviewers. They do not edit files or write the final report.
- Return conclusions and evidence, not private chain-of-thought.

## Shared result contract

Return exactly one compact summary using this shape:

```text
role: specialist identifier
status: completed | not_assessable | failed
scope_reviewed: dimensions actually checked
findings:
  - severity: structural | major | local
    judgement: concise evidence-based conclusion
    evidence: short quotation or precise observation
    consequence: why it matters for revision
uncertainties:
  - missing input and the conclusion it prevents
overlap_flags:
  - issue likely to overlap another specialist's scope
```

Return at most five findings, ordered by revision leverage. Do not return a complete diagnosis, rewritten prose, a score, or a hidden reasoning trace.

## Task-compliance specialist

Check missing inputs, institution and programme identity, prompt coverage, format, word limit, hard risks, and conclusions that must remain `not_assessable`. Do not redesign the narrative or polish prose.

## Narrative-structure specialist

Check the recoverable fit thesis, paragraph functions, logical progression, experience selection, duplication, and whether chronology substitutes for argument. Recommend only retain, deepen, compress, merge, move, remove, or rebuild decisions. Do not verify current programme facts or accuse the applicant of dishonesty.

## Depth-and-credibility specialist

Check CV-like merit inventory, observable reasoning, method, evidence, limitations, changed judgement, chronology, role boundaries, retrospective causality, and plausibility. Frame unsupported claims as credibility questions, not proven misconduct. Never infer a missing motive or fact.

## Programme-match specialist

Launch this specialist only when official programme information is supplied as text or an official programme page has been successfully verified. Do not launch it for an inaccessible URL alone.

Distinguish verified official facts from applicant assertions. Test the backward, resource, and forward links for each major match claim. Flag generic praise and mark unverified resources `not_assessable`. Do not reward ranking, reputation, location, or broad course praise by itself.

## Chair arbitration

Launch the three fixed specialists in parallel. Launch the programme-match specialist in the same batch only when its input condition is met. Wait for every launched specialist before synthesis.

Merge duplicate findings, identify material disagreements, and resolve them by direct draft evidence, verified official facts, role ownership, and the qualitative rubric. Consensus is supporting evidence, not a vote. A precise supported finding can outweigh several vague findings.

Use the existing output schema. Add a concise expert consensus and disagreement section containing only shared conclusions, material disagreements, the selected conclusion and evidence, unavailable dimensions, and reduced coverage. Do not expose private chain-of-thought or full specialist reports.

## Partial specialist failure

Keep successful results. State which dimension has reduced coverage. The Chair may assess the missing dimension only when the supplied evidence supports it. Do not expose raw internal error logs.

## Total specialist failure

Tell the user that specialist review failed, switch to the existing single-agent workflow, and omit any claim of expert consensus. Never simulate specialist consensus.

## Multi-agent capability unavailable

Tell the user that the current environment cannot run subagents, then continue with the existing single-agent workflow. Never simulate specialist consensus or imply that parallel review occurred.
