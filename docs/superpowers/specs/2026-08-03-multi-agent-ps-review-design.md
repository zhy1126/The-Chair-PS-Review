# Multi-Agent PS Review Design

## Summary

Upgrade The Chair from a single-agent serial review into a portable, single-Skill workflow that delegates independent diagnostic dimensions to specialist subagents in parallel. The primary agent remains the Chair: it prepares the shared review context, launches specialists, reconciles their evidence, and produces the existing unified diagnosis.

The upgrade must preserve the current public interface and editorial boundaries:

- Users continue to invoke `$the-chair-ps-review`.
- Installation still requires copying only one Skill directory.
- The workflow diagnoses and guides; it does not ghostwrite.
- It does not invent applicant facts, programme facts, causal links, or reflections.
- It does not produce a default numerical score.

## Goals

1. Improve diagnostic coverage by assigning distinct dimensions to focused specialists.
2. Run independent reviews in parallel to reduce avoidable latency.
3. Make the final judgement auditable through concise evidence, consensus, disagreement, and arbitration notes.
4. Preserve a usable single-agent fallback when subagents are unavailable or fail.
5. Keep the repository distributable as one standalone Codex Skill without separate custom-agent installation.

## Non-goals

- Shipping project-scoped or user-scoped `.codex/agents/*.toml` files.
- Building an external orchestration service or MCP server.
- Exposing private chain-of-thought or complete internal specialist transcripts.
- Replacing the existing qualitative rubric or wholesale replacing its output schema; a small transparency extension is in scope.
- Adding essay rewriting, application prediction, or automatic numerical scoring.

## Architecture

The primary agent performs intake and acts as Chair. Once the workflow has enough material to begin either a full diagnosis or a user-requested provisional precheck, it creates generic subagents at runtime with bounded role instructions packaged in the Skill. Three specialists run when multi-agent capability is available. A fourth runs only when official programme information is supplied as text or an official programme page is successfully verified. Merely supplying an inaccessible URL does not start the fourth specialist.

```text
User materials
  -> primary-agent intake and context preparation
     -> task-compliance specialist -----------\
     -> narrative-structure specialist --------+-> Chair arbitration -> unified diagnosis
     -> depth-and-credibility specialist ------+
     -> programme-match specialist (conditional)/
```

Subagents are read-only reviewers. They do not edit files, contact third parties, or write the final user-facing report. The Chair waits for all requested specialists before synthesising results.

## Specialist responsibilities

### Task-compliance specialist

Responsible for:

- missing required inputs and resulting review limitations;
- institution, programme, prompt, format, and word-limit consistency;
- hard requirement violations and obvious factual inconsistencies;
- whether a conclusion must be marked `not assessable`.

It does not redesign the narrative or polish prose.

### Narrative-structure specialist

Responsible for:

- the recoverable fit thesis;
- paragraph functions and progression;
- experience selection, duplication, and opportunity cost;
- whether chronology or juxtaposition substitutes for logic;
- retain, deepen, compress, merge, move, remove, or rebuild decisions.

It does not verify current programme facts or declare an applicant dishonest.

### Depth-and-credibility specialist

Responsible for:

- CV-like merit inventory patterns;
- observable reasoning, method, evidence, limitations, and changed judgement;
- chronology, role boundaries, retrospective causality, and plausibility risks;
- prestige signals and action verbs that replace reflection.

It flags unsupported claims as credibility questions, not proven misconduct, and never invents a motive or missing fact.

### Programme-match specialist

This specialist starts only when the user supplies official programme information or an official programme page can be verified.

Responsible for:

- distinguishing verified official facts from applicant assertions;
- checking backward, resource, and forward links for major match claims;
- identifying generic praise and transferable programme language;
- marking unavailable or unverified resources as `not assessable`.

If no official information is available, the Chair records programme match as not assessable instead of launching this specialist solely to restate the missing input.

### Chair

The primary agent acts as Chair and is responsible for:

- preparing a minimal shared context from the intake;
- launching applicable specialists in parallel and waiting for them;
- deduplicating overlapping findings;
- resolving differences by evidence strength rather than vote count;
- choosing issue severity and exactly three revision priorities in dependency order;
- producing the final report using the existing output schema;
- adding a concise expert consensus and disagreement section.

The Chair may apply the existing rubric to specialist evidence, but it must not introduce unverified facts that no specialist or source established.

## Specialist result contract

Each specialist returns a compact structured summary with these fields:

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

Each specialist returns at most five findings and prioritises the highest-leverage issues. It must not return a complete diagnosis, rewritten paragraph, numerical score, or hidden reasoning trace.

## Data flow

1. The primary agent loads the existing intake, evaluation philosophy, rubric, and output requirements.
2. It classifies the task and identifies missing inputs before delegation.
3. If required inputs are missing, it asks for them and delegates only after the user supplies them or explicitly chooses a provisional precheck.
4. It prepares the shared context: application type, programme, prompt, limits, applicant background, draft, official programme information, and known review limitations.
5. It launches the three fixed specialists concurrently and conditionally launches the programme-match specialist.
6. It waits for all requested results and records completed, not-assessable, and failed statuses.
7. It normalises valid findings, merges duplicates, and identifies disagreements.
8. It arbitrates using direct textual or official-source evidence, then writes the existing eleven-section report.
9. It appends a concise `Expert consensus and disagreement` section.

Only information needed for a specialist's assigned dimension should be included in its task. Personal identifiers that do not affect the review should be removed or masked before delegation.

## Arbitration and transparency

The transparency section is deliberately short and does not reveal private chain-of-thought. It contains only:

- conclusions supported by more than one specialist;
- material disagreements between specialists;
- the Chair's selected conclusion and the short evidence supporting that choice;
- dimensions that remain not assessable because of missing information;
- any specialist failure that reduced coverage.

The target length is approximately 150 Chinese characters or a similarly compact amount in the user's language. The section can be shorter when there is no meaningful disagreement.

Consensus is supporting evidence, not a vote. A finding supported by a precise quotation or verified official fact can outweigh a broader majority claim with weak evidence.

## Failure and fallback behaviour

### Multi-agent capability unavailable

The primary agent tells the user that the environment cannot run subagents and continues with the existing single-agent diagnostic workflow. It does not imply that expert consensus occurred.

### One specialist fails

The Chair keeps successful results, identifies the uncovered dimension, and assesses it itself only when the supplied evidence allows. The final transparency note names the reduced coverage without exposing internal error logs.

### All specialists fail

The Chair explicitly switches to the existing single-agent workflow. The final response describes the fallback and omits any expert-consensus claim.

### Official programme page unavailable

The workflow does not guess current modules, faculty, requirements, or resources. Programme match is marked not assessable unless the user supplied adequate official information directly.

### Conflicting findings

The Chair compares the quoted text, official sources, scope ownership, and rubric definitions. It records only material conflicts and explains the selected conclusion with concise evidence.

## Output changes

The existing eleven-part diagnostic report remains the canonical output. Add one final section:

```markdown
## 12. Expert consensus and disagreement

- Consensus: ...
- Disagreement and Chair decision: ...
- Not assessable or reduced coverage: ...
```

Omit empty bullets. When multi-agent execution was unavailable or fully failed, replace this section with a one-sentence fallback disclosure rather than simulated consensus.

## Repository changes

The implementation is expected to remain instruction-first:

- revise `skill/the-chair-ps-review/SKILL.md` to define orchestration, parallel launch, waiting, arbitration, and fallback;
- add specialist role instructions and the result contract under `skill/the-chair-ps-review/references/`;
- revise `references/output-schema.md` to add the transparency section;
- update `README.md` to explain the multi-agent workflow, conditional programme specialist, token-cost expectation, and fallback;
- add repository-level validation and scenario tests for the Skill instructions and contracts.

No external service, custom-agent installation, or separate user configuration is required.

## Test strategy

### Static validation

Check that:

- the Skill metadata and referenced files are present;
- every referenced specialist role exists;
- the result-status and severity enums remain consistent across files;
- the output schema contains the transparency section;
- the Skill retains the no-ghostwriting, no-invention, and no-default-score boundaries.

### Scenario tests

Use representative, synthetic prompts to verify these behaviours:

1. Complete context with official programme information launches four specialists.
2. Missing official programme information launches only the three fixed specialists and marks programme match not assessable.
3. One specialist failure produces reduced-coverage disclosure and a usable final report.
4. All specialists failing produces an explicit single-agent fallback without simulated consensus.
5. Conflicting findings are resolved using quoted evidence rather than vote count.
6. Missing intake fields remain limitations instead of negative judgements.
7. Requests for a complete rewrite, invented experience, or default numerical score remain refused or redirected.
8. Final transparency remains concise and contains no full specialist reports or hidden reasoning trace.

### Manual acceptance check

Run the Skill on at least one synthetic CV-like draft and one focused fit narrative. Confirm that the multi-agent result remains compatible with the existing calibration cases and that the Chair's three revision priorities are coherent, non-duplicative, and evidence-based.

## Acceptance criteria

The feature is ready when:

- one installed Skill can trigger the complete workflow in a multi-agent-enabled Codex environment;
- the three fixed specialists run independently and the programme specialist follows the conditional rule;
- specialist outputs follow the compact result contract;
- the Chair produces one unified report with concise, evidence-based arbitration notes;
- partial and total failures degrade transparently without blocking a diagnosis;
- existing evaluation boundaries and qualitative classifications remain intact;
- automated validation passes and representative manual scenarios show no fabricated facts, ghostwriting, or simulated consensus.
