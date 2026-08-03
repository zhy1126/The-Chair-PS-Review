# PS Diagnostic Report

Use this structure unless the user requests a narrower review.

## 1. Review basis

List the draft, application category, essay type, exact prompt, word limit, target programme, official programme information, CV/background, and intended direction received. State missing inputs and resulting limitations.

## 2. One-sentence verdict

Classify the draft as a convincing fit argument, promising but incomplete trajectory, CV-like merit inventory, generic motivation essay, or structurally mispositioned response. Name the highest-leverage issue immediately.

## 3. Fit thesis

Write the fit thesis in schematic language, not polished submission prose:

`trajectory/question → training need → programme resource → future use`

If a link is missing or cannot be assessed from the supplied context, mark it explicitly.

## 4. Structural risk

List hard risks and classify issues as structural, major, or local. Explain why sentence polishing should or should not begin yet.

## 5. Qualitative diagnostic map

| Dimension | Classification | Evidence | Consequence or main action |
|---|---|---|---|
| Positioning and match | Convincing / Developing / Structural risk / Not assessable | Short quotation or observation | Action |
| Main line and progression | Classification | Evidence | Action |
| Depth of thought | Classification | Evidence | Action |
| Experience selection and evidence | Classification | Evidence | Action |
| Task compliance and professionalism | Classification | Evidence | Action |

Do not provide a weighted total or default numerical score. Missing context must produce `not assessable`, not a penalty.

## 6. Main-line map

Map each paragraph:

| Paragraph | Current function | Contribution to main line | Connection problem | Decision |
|---|---|---|---|---|

Use decisions such as retain, deepen, compress, merge, move, remove, or rebuild. Show which paragraphs are essential, duplicative, detachable, or misplaced.

## 7. CV-versus-PS audit

Identify achievements repeated from the CV/transcript, experiences that receive insufficient depth, material to retain or reduce, and prestige signals that do not earn their word cost. If no CV was supplied, state that duplication cannot be fully checked.

## 8. Programme-match audit

For each major programme claim, test the backward, resource, and forward links. Flag generic praise and unverified programme details. Do not invent programme resources.

## 9. Three revision priorities

Give exactly three high-leverage tasks in dependency order. Describe the decision and required evidence, not the final prose.

## 10. Questions for the applicant

Ask no more than three focused questions that recover missing reflection, evidence, chronology, limitation, or match.

## 11. Self-revision checklist

Include a concise checklist tailored to the draft before the final transparency section.

## 12. Expert consensus and disagreement

Keep this section to approximately 150 Chinese characters or a similarly compact amount in the user's language. Omit empty items.

- **Consensus:** Include only material conclusions supported by more than one specialist.
- **Disagreement and Chair decision:** State the competing conclusions, the selected conclusion, and the decisive short evidence. Resolve by evidence, not vote count.
- **Not assessable or reduced coverage:** Name missing inputs or failed specialist dimensions that materially limit the diagnosis.

Do not expose private chain-of-thought or append complete specialist reports.

This section consumes only normalized specialist summaries whose contract has exactly `role`, `status`, `source_provenance`, `scope_reviewed`, `findings`, `uncertainties`, and `overlap_flags`. Preserve `source_provenance` in programme claims and arbitration: user-pasted official-looking text is `pasted_user_supplied_official_text`, not independent verification; only a successfully accessed official page is `verified_official_page`.

Use these section-specific branches after every requested role has returned or been normalized:

| Completed roles after normalization | Non-completed roles after normalization | Required path |
|---|---|---|
| All requested roles | None | Normal multi-agent synthesis. |
| At least one | At least one | Partial coverage: use only `completed` findings and disclose every non-completed dimension and status. |
| Zero | All requested roles | Explicit single-agent fallback regardless of the `failed`/`not_assessable` mix; do not claim consensus. |

For at least one `completed` and at least one non-completed role, use findings only from `completed` roles and name every non-completed dimension and status (`not_assessable` or `failed`) under reduced coverage. For zero `completed` roles, replace this section with a one-sentence single-agent fallback disclosure; do not preserve or imply successful specialist results.

When multi-agent capability was unavailable, use the same one-sentence fallback disclosure and do not claim expert consensus.

Do not provide a full rewritten paragraph or essay. If an illustration is essential, use placeholders such as `[specific observation] → [question] → [method] → [changed judgement]`.

