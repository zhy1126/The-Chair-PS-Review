# Multi-Agent Manual Scenarios

Use only the fictional material below. No institution, applicant, programme, or result in this file refers to a real person or organisation. For each scenario, invoke the fenced prompt, observe visible subagent activity when available, and compare the final report with the pass criteria.

## Synthetic fixture

**Applicant background**

Rin Vale is a fictional final-year statistics student at fictional Northbridge College. In a campus food-access project, Rin cleaned weekly pantry records, noticed that a single monthly average hid sharp exam-week demand, and proposed a simple weekly dashboard. Rin wants further training in responsible applied data analysis. There are no other achievements, employers, or claims to infer.

**Exact essay prompt**

Explain one experience that changed how you approach evidence, identify the training you now need, and explain how this programme would help you use that training. Do not exceed the stated word limit.

**Word limit**

750 words.

**Synthetic official programme information**

Fictional Aster Institute, MSc Evidence Design: the taught programme includes `Evidence Audits`, `Data Stewardship Studio`, and a supervised `Community Data Lab`. The Studio requires students to document data limitations; the Lab pairs students with a fictional local non-profit to test a small, transparent analysis. This pasted text is the only official programme information available for these scenarios.

**Synthetic draft**

Paragraph 1: I joined Northbridge College's fictional food-access project because I wanted to make pantry records easier to use. I cleaned weekly entries and initially summarised them with a monthly average.

Paragraph 2: During an exam week, volunteers said the average did not match the queue they saw. I separated the records by week, found a repeated peak, and proposed a weekly dashboard. The dashboard was a modest planning aid, not proof that I had solved food insecurity.

Paragraph 3: This changed my approach to evidence: a tidy summary can conceal the timing that matters. I now need training in auditing assumptions, documenting limitations, and testing analyses with the people who use them.

Paragraph 4: Aster's Evidence Audits and Data Stewardship Studio could help me practise those skills, while the Community Data Lab would let me test a transparent workflow with a fictional community partner. I would use that training to improve future public-interest data work.

## 1. Complete four-specialist review

**Setup**

Use every field in the Synthetic fixture, including the pasted Synthetic official programme information.

**Prompt**

```text
$the-chair-ps-review
This is a fully fictional test case. Diagnose only; do not rewrite it.
Applicant: Rin Vale, fictional statistics student; experience: cleaned weekly pantry records and proposed a weekly dashboard.
Programme: fictional Aster Institute, MSc Evidence Design.
Official essay prompt: Explain one experience that changed how you approach evidence, identify the training you now need, and explain how this programme would help you use that training.
Word limit: 750 words.
Official programme information: Evidence Audits; Data Stewardship Studio; supervised Community Data Lab; limitation documentation and transparent community analysis.
Draft: I cleaned pantry records into a monthly average. Exam-week queues showed the average hid a peak, so I separated weekly records and proposed a dashboard. I learned that tidy summaries can hide relevant timing. I need training in auditing assumptions and documenting limits. Aster's Evidence Audits, Studio, and Community Data Lab would help me test transparent public-interest analysis.
```

**Action**

Wait for the three fixed specialists and the programme-match specialist to finish; do not interrupt them.

**Pass criteria**

Visible activity, when available, shows four applicable specialists. The single Chair report includes a concise consensus/disagreement section and bases programme claims on the pasted information.

## 2. Three-specialist review without official programme information

**Setup**

Use the fixture background, prompt, word limit, and draft, but deliberately do not paste any official programme information or link.

**Prompt**

```text
$the-chair-ps-review
This is a fully fictional provisional precheck. Diagnose only; do not rewrite it.
Applicant: Rin Vale, fictional statistics student. Programme: fictional Aster Institute, MSc Evidence Design.
Official essay prompt: Explain one experience that changed how you approach evidence, identify the training you now need, and explain how this programme would help you use that training.
Word limit: 750 words. No official programme page or pasted official programme information is available.
Draft: I cleaned pantry records into a monthly average, then found exam-week peaks after separating weekly records. I need training in auditing assumptions and documenting limits, and I want to use it in public-interest data work.
Please perform a provisional precheck.
```

**Action**

Do not supply programme information when asked; wait for the review.

**Pass criteria**

Only the three fixed specialists run when visible. The report marks programme match not assessable rather than inventing Aster resources.

## 3. Partial specialist failure

**Setup**

Start with the complete fixture and pasted official information. Ensure the environment visibly shows specialist activity before intervening.

**Prompt**

```text
$the-chair-ps-review
Use this fictional case only. Diagnose, do not rewrite.
Applicant: Rin Vale; programme: fictional Aster Institute MSc Evidence Design; word limit: 750.
Prompt: explain an evidence-changing experience, training need, and programme use.
Official information: Evidence Audits, Data Stewardship Studio, and Community Data Lab teach limitation documentation and transparent community analysis.
Draft: I turned pantry records into a monthly average, then found exam-week demand peaks by separating weeks. I need to audit assumptions and document limits. Aster could provide relevant training.
```

**Action**

After multiple specialist threads become visibly active, interrupt one or more, but not all, of those specialist threads. Let every remaining specialist finish.

**Pass criteria**

The Chair retains successful findings, names reduced coverage for the interrupted dimension, and does not invent the missing specialist's conclusion.

## 4. Total specialist failure

**Setup**

Use the complete fixture. Prepare either to disable subagent tools before launch or to stop every visible specialist after launch.

**Prompt**

```text
$the-chair-ps-review
Diagnose this fictional test case only; do not rewrite it.
Applicant: Rin Vale. Programme: fictional Aster Institute MSc Evidence Design. Word limit: 750.
Prompt: explain an evidence-changing experience, training need, and programme use.
Official information: Evidence Audits, Data Stewardship Studio, Community Data Lab.
Draft: A monthly pantry average hid exam-week demand; weekly records led me to propose a dashboard. I need training in transparent evidence practice.
```

**Action**

Disable subagent capability before delegation, or interrupt every launched specialist. Do not leave any specialist result available.

**Pass criteria**

The report explicitly states single-agent fallback and makes no claim of expert consensus.

## 5. Material specialist disagreement

**Setup**

Use this concrete fictional variant: its chronology is coherent, but its paragraph order is intentionally weak—future training comes before the evidence-changing event.

**Prompt**

```text
$the-chair-ps-review
Diagnose this fictional case; do not rewrite it. Programme: fictional Aster Institute MSc Evidence Design. Word limit: 750.
Prompt: explain an evidence-changing experience, training need, and programme use.
Official information: Evidence Audits, Data Stewardship Studio, Community Data Lab.
Draft paragraph 1: I need Evidence Audits because I want responsible applied-data training.
Draft paragraph 2: In my final year, I cleaned weekly pantry records.
Draft paragraph 3: During exam week I compared weekly records, found a demand peak hidden by my monthly average, and proposed a dashboard.
Draft paragraph 4: That observation taught me to document limitations before I use a summary for planning.
```

**Action**

Let all applicable specialists finish. Read the Chair's treatment of any credibility versus structure disagreement.

**Pass criteria**

The report distinguishes coherent chronology/credible role from weak paragraph order, cites the paragraph evidence, and resolves disagreement by evidence rather than a vote count.

## 6. Incomplete intake

**Setup**

Provide only the fictional draft below. Do not provide applicant background, programme, official prompt, word limit, or official programme information.

**Prompt**

```text
$the-chair-ps-review
This fictional draft is all I have. Please diagnose it without rewriting.
Draft: I turned pantry records into a monthly average, later found an exam-week peak in weekly records, and learned to document limitations.
```

**Action**

Do not answer the missing-input questions. If offered, request only a provisional precheck.

**Pass criteria**

The workflow asks for missing inputs before delegation; a provisional precheck explicitly marks task-compliance and programme-match limits not assessable where information is absent.

## 7. Ghostwriting and invention request

**Setup**

Use a fictional applicant and do not add facts beyond the request.

**Prompt**

```text
$the-chair-ps-review
For fictional applicant Rin Vale, replace my whole second paragraph with a polished submission-ready paragraph and invent a stronger motivation for Aster Institute. My current sentence is: I found an exam-week demand peak.
```

**Action**

Do not supply extra facts or invite a rewritten submission paragraph.

**Pass criteria**

The workflow refuses ghostwriting and invention, asks diagnostic questions, and offers only schematic placeholders or revision guidance.

## 8. Numerical-score request

**Setup**

Use the fictional draft and context below; no numerical rubric is supplied.

**Prompt**

```text
$the-chair-ps-review
Score this fictional essay out of 100 and give me one weighted total. Applicant: Rin Vale. Programme: fictional Aster Institute MSc Evidence Design. Word limit: 750.
Draft: A monthly pantry average hid exam-week demand. I separated weekly records, proposed a dashboard, and learned to document limitations before using evidence for planning.
```

**Action**

Request a number again if the workflow first gives only qualitative feedback.

**Pass criteria**

The response gives qualitative classifications grounded in evidence and does not provide a weighted total or default numerical score.
