# Multi-Agent PS Review Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Upgrade `$the-chair-ps-review` so three fixed specialist subagents and one conditional programme specialist review a PS in parallel before the primary Chair produces one transparent, evidence-based diagnosis.

**Architecture:** Keep the project as one portable instruction-first Skill. Put bounded role cards, the shared result contract, arbitration rules, and fallbacks in one new protocol reference; make `SKILL.md` own runtime orchestration; extend the existing report schema with a concise arbitration section. Validate the instruction contract with dependency-free Python tests and document manual Codex scenarios for behavior that static tests cannot execute.

**Tech Stack:** Markdown Agent Skill instructions, YAML UI metadata, Python 3 standard-library `unittest`, Git.

---

## File map

- Create `skill/the-chair-ps-review/references/multi-agent-protocol.md`: single source of truth for specialist roles, launch conditions, result shape, arbitration, privacy, and fallback.
- Modify `skill/the-chair-ps-review/SKILL.md`: decide when to delegate, launch applicable specialists in parallel, wait, arbitrate, and degrade explicitly.
- Modify `skill/the-chair-ps-review/references/output-schema.md`: add the compact expert consensus/disagreement section.
- Modify `skill/the-chair-ps-review/agents/openai.yaml`: describe the multi-agent behavior in the visible metadata and default prompt.
- Modify `README.md`: explain architecture, conditional programme specialist, transparency, cost, fallback, and unchanged installation.
- Create `tests/test_multi_agent_skill.py`: static contract tests for the instruction artifacts.
- Create `tests/manual-scenarios.md`: synthetic end-to-end Codex smoke scenarios and expected observable behavior.

### Task 1: Define and validate the specialist protocol

**Files:**
- Create: `tests/test_multi_agent_skill.py`
- Create: `skill/the-chair-ps-review/references/multi-agent-protocol.md`

- [ ] **Step 1: Write the failing protocol contract tests**

Create `tests/test_multi_agent_skill.py` with:

```python
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

    def test_protocol_makes_programme_review_conditional_and_defines_fallbacks(self) -> None:
        protocol = read(PROTOCOL)
        self.assertIn("Do not launch it for an inaccessible URL alone", protocol)
        self.assertIn("## Partial specialist failure", protocol)
        self.assertIn("## Total specialist failure", protocol)
        self.assertIn("## Multi-agent capability unavailable", protocol)
        self.assertIn("Never simulate specialist consensus", protocol)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the tests and verify the intended failure**

Run:

```bash
python3 -m unittest discover -s tests -p 'test_multi_agent_skill.py' -v
```

Expected: two failures because `references/multi-agent-protocol.md` does not exist.

- [ ] **Step 3: Add the minimal complete multi-agent protocol**

Create `skill/the-chair-ps-review/references/multi-agent-protocol.md` with:

```markdown
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
```

- [ ] **Step 4: Run the protocol tests and verify they pass**

Run:

```bash
python3 -m unittest discover -s tests -p 'test_multi_agent_skill.py' -v
```

Expected: two tests pass.

- [ ] **Step 5: Commit the protocol and tests**

```bash
git add tests/test_multi_agent_skill.py skill/the-chair-ps-review/references/multi-agent-protocol.md
git commit -m "feat: define multi-agent review protocol"
```

### Task 2: Make the Skill orchestrate parallel specialists

**Files:**
- Modify: `tests/test_multi_agent_skill.py`
- Modify: `skill/the-chair-ps-review/SKILL.md:33-105`

- [ ] **Step 1: Add failing orchestration tests**

Add this class above the `if __name__ == "__main__"` block in `tests/test_multi_agent_skill.py`:

```python
class SkillOrchestrationTests(unittest.TestCase):
    def test_skill_loads_protocol_launches_in_parallel_and_waits(self) -> None:
        skill = read(SKILL)
        self.assertIn("Read `references/multi-agent-protocol.md`", skill)
        self.assertIn("Launch all applicable specialists in parallel", skill)
        self.assertIn("Wait for every launched specialist", skill)
        self.assertIn("The primary agent remains the Chair", skill)

    def test_skill_uses_conditional_programme_specialist_and_explicit_fallback(self) -> None:
        skill = read(SKILL)
        self.assertIn("Do not launch the programme-match specialist", skill)
        self.assertIn("official programme information", skill)
        self.assertIn("tell the user before falling back", skill.lower())
        self.assertIn("Never claim expert consensus after a full fallback", skill)
```

- [ ] **Step 2: Run the tests and verify the new tests fail**

Run:

```bash
python3 -m unittest discover -s tests -p 'test_multi_agent_skill.py' -v
```

Expected: the two protocol tests pass and the two orchestration tests fail because `SKILL.md` does not yet contain the orchestration contract.

- [ ] **Step 3: Load the protocol as part of the evaluation standard**

In `skill/the-chair-ps-review/SKILL.md`, add this bullet after the existing `output-schema.md` bullet:

```markdown
- Read `references/multi-agent-protocol.md` for specialist roles, parallel dispatch, result contracts, arbitration, privacy, and fallback behaviour.
```

- [ ] **Step 4: Add the orchestration section before the current diagnostic workflow**

Insert this section immediately before `## Run the diagnostic workflow`:

```markdown
## Orchestrate the multi-agent diagnosis

The primary agent remains the Chair. Delegate only after the required intake is complete or the user explicitly accepts a provisional text-only precheck.

Prepare the smallest sufficient shared context: application type, document type, institution and programme, exact prompt, word limit, applicant background, draft, verified or pasted official programme information, and known limitations. Remove or mask identifiers that are unnecessary for review.

When subagent tools are available:

1. Launch all applicable specialists in parallel using the bounded role instructions and result contract in `references/multi-agent-protocol.md`.
2. Always launch the task-compliance, narrative-structure, and depth-and-credibility specialists.
3. Launch the programme-match specialist only when official programme information was pasted by the user or an official page was successfully verified. Do not launch the programme-match specialist for an inaccessible URL alone.
4. Wait for every launched specialist before synthesising the diagnosis.
5. Treat specialist conclusions as evidence, not votes. Resolve overlap and conflict with the draft, verified programme facts, role ownership, and `references/rubric.md`.

If subagent tools are disabled, unavailable, or every specialist fails, tell the user before falling back to the existing single-agent diagnostic workflow below. Never claim expert consensus after a full fallback. If only one specialist fails, preserve successful results and disclose the reduced coverage in the final transparency section.

Do not expose private chain-of-thought or append full specialist reports. The Chair writes one report only.
```

- [ ] **Step 5: Make the existing diagnostic steps the Chair's synthesis checklist**

Replace the heading `## Run the diagnostic workflow` with:

```markdown
## Apply the diagnostic and synthesis checklist

Use the following steps as the shared diagnostic standard and as the Chair's synthesis checklist. Do not perform a duplicate full review before launching specialists.
```

Keep the existing numbered subsections `### 1. Classify the task` through `### 9. Prioritise revision` unchanged below it.

- [ ] **Step 6: Run the full contract tests**

Run:

```bash
python3 -m unittest discover -s tests -p 'test_multi_agent_skill.py' -v
```

Expected: four tests pass.

- [ ] **Step 7: Commit the Skill orchestration**

```bash
git add tests/test_multi_agent_skill.py skill/the-chair-ps-review/SKILL.md
git commit -m "feat: orchestrate parallel PS review specialists"
```

### Task 3: Extend the report with concise arbitration transparency

**Files:**
- Modify: `tests/test_multi_agent_skill.py`
- Modify: `skill/the-chair-ps-review/references/output-schema.md:62-66`

- [ ] **Step 1: Add failing output contract tests**

Add this class above the `if __name__ == "__main__"` block in `tests/test_multi_agent_skill.py`:

```python
class OutputTransparencyTests(unittest.TestCase):
    def test_output_schema_adds_concise_evidence_based_arbitration(self) -> None:
        schema = read(OUTPUT_SCHEMA)
        self.assertIn("## 12. Expert consensus and disagreement", schema)
        self.assertIn("approximately 150 Chinese characters", schema)
        self.assertIn("evidence, not vote count", schema)
        self.assertIn("Do not expose private chain-of-thought", schema)

    def test_output_schema_never_simulates_consensus_after_fallback(self) -> None:
        schema = read(OUTPUT_SCHEMA)
        self.assertIn("one-sentence fallback disclosure", schema)
        self.assertIn("do not claim expert consensus", schema)
```

- [ ] **Step 2: Run tests and verify the output tests fail**

Run:

```bash
python3 -m unittest discover -s tests -p 'test_multi_agent_skill.py' -v
```

Expected: four earlier tests pass and two output tests fail.

- [ ] **Step 3: Add section 12 to the output schema**

Append this section to `skill/the-chair-ps-review/references/output-schema.md` before its final no-rewrite reminder:

```markdown
## 12. Expert consensus and disagreement

Keep this section to approximately 150 Chinese characters or a similarly compact amount in the user's language. Omit empty items.

- **Consensus:** Include only material conclusions supported by more than one specialist.
- **Disagreement and Chair decision:** State the competing conclusions, the selected conclusion, and the decisive short evidence. Resolve by evidence, not vote count.
- **Not assessable or reduced coverage:** Name missing inputs or failed specialist dimensions that materially limit the diagnosis.

Do not expose private chain-of-thought or append complete specialist reports.

When multi-agent capability was unavailable or every specialist failed, replace this section with a one-sentence fallback disclosure and do not claim expert consensus.
```

- [ ] **Step 4: Run tests and verify all six pass**

Run:

```bash
python3 -m unittest discover -s tests -p 'test_multi_agent_skill.py' -v
```

Expected: six tests pass.

- [ ] **Step 5: Commit the transparency contract**

```bash
git add tests/test_multi_agent_skill.py skill/the-chair-ps-review/references/output-schema.md
git commit -m "feat: add transparent Chair arbitration output"
```

### Task 4: Document user-visible behavior and manual scenarios

**Files:**
- Modify: `tests/test_multi_agent_skill.py`
- Create: `tests/manual-scenarios.md`
- Modify: `README.md:5-43,96-140`
- Modify: `skill/the-chair-ps-review/agents/openai.yaml:1-4`

- [ ] **Step 1: Add failing documentation and scenario tests**

Add this class above the `if __name__ == "__main__"` block in `tests/test_multi_agent_skill.py`:

```python
class DocumentationTests(unittest.TestCase):
    def test_readme_documents_multi_agent_cost_condition_and_fallback(self) -> None:
        readme = read(README)
        self.assertIn("## 多 Agent 工作方式", readme)
        self.assertIn("任务合规专家", readme)
        self.assertIn("主线结构专家", readme)
        self.assertIn("深度真实性专家", readme)
        self.assertIn("项目匹配专家", readme)
        self.assertIn("只有在官方项目资料可用时", readme)
        self.assertIn("会消耗更多 token", readme)
        self.assertIn("降级为单 Agent", readme)
        self.assertIn("无需额外安装", readme)

    def test_visible_metadata_mentions_parallel_expert_review(self) -> None:
        metadata = read(OPENAI_YAML)
        self.assertIn("多专家并行", metadata)
        self.assertIn("由 Chair 仲裁", metadata)

    def test_manual_scenarios_cover_runtime_and_safety_boundaries(self) -> None:
        self.assertTrue(MANUAL_SCENARIOS.exists(), "manual scenario matrix is missing")
        scenarios = read(MANUAL_SCENARIOS)
        for heading in (
            "## 1. Complete four-specialist review",
            "## 2. Three-specialist review without official programme information",
            "## 3. Partial specialist failure",
            "## 4. Total specialist failure",
            "## 5. Material specialist disagreement",
            "## 6. Incomplete intake",
            "## 7. Ghostwriting and invention request",
            "## 8. Numerical-score request",
        ):
            self.assertIn(heading, scenarios)
```

- [ ] **Step 2: Run tests and verify the three new tests fail**

Run:

```bash
python3 -m unittest discover -s tests -p 'test_multi_agent_skill.py' -v
```

Expected: six earlier tests pass and three documentation tests fail.

- [ ] **Step 3: Add the README multi-agent explanation**

Insert this section after `## 核心理念` and its bullet list in `README.md`:

```markdown
## 多 Agent 工作方式

一次完整诊断由主 Agent 担任 Chair，并行调度边界清晰的专家：

- **任务合规专家**：检查材料缺口、题目、字数和硬性要求；
- **主线结构专家**：检查契合主张、段落功能、逻辑推进和经历取舍；
- **深度真实性专家**：检查 CV 化、思考深度、时间线、职责和因果可信度；
- **项目匹配专家**：核验项目资源及其与申请者训练需求的关系，只有在官方项目资料可用时才启动。

Chair 等待专家结果后，按文本证据和官方事实仲裁，而不是简单投票。最终报告只增加简洁的“专家共识与分歧”，不会展示内部思维链或堆叠多份重复报告。

多 Agent 审查会消耗更多 token。若当前 Codex 环境未启用子 Agent，或全部专家运行失败，Skill 会明确提示并降级为单 Agent，不会伪造专家共识。安装方式不变，无需额外安装自定义 Agent。
```

Add item 12 to the existing output list:

```markdown
12. 简洁的专家共识、分歧与 Chair 仲裁依据。
```

After the installation invocation example, add:

```markdown
多 Agent 编排包含在 Skill 指令中，无需把 `.toml` Agent 配置复制到其他目录。当前 Codex 环境若支持子 Agent，会自动使用并行专家流程；否则会明确降级。
```

- [ ] **Step 4: Update the visible Skill metadata**

Replace `skill/the-chair-ps-review/agents/openai.yaml` with:

```yaml
interface:
  display_name: "The Chair｜多 Agent PS 契合度诊断"
  short_description: "多专家并行检查契合、主线、深度与真实性，并由 Chair 仲裁"
  default_prompt: "使用 $the-chair-ps-review 先收集项目、官网、题目、字数和文书，再让多专家并行定性诊断并由 Chair 仲裁；只指导不代写。"
```

- [ ] **Step 5: Add the manual scenario matrix**

Create `tests/manual-scenarios.md` with:

```markdown
# Multi-Agent Manual Scenarios

Use only synthetic application material. For each scenario, invoke `$the-chair-ps-review`, observe visible subagent activity when available, and compare the final report with the expected behavior.

## 1. Complete four-specialist review

Provide a synthetic draft, CV summary, exact prompt and word limit, plus pasted official programme information. Expect three fixed specialists and the programme-match specialist, one Chair report, and a concise consensus/disagreement section.

## 2. Three-specialist review without official programme information

Provide the same material without an accessible official page or pasted official information and explicitly request a provisional precheck. Expect only the three fixed specialists and programme match marked not assessable.

## 3. Partial specialist failure

Interrupt one active specialist. Expect the Chair to retain other results, disclose reduced coverage, and avoid inventing the missing specialist's conclusion.

## 4. Total specialist failure

Disable multi-agent tools or interrupt every specialist. Expect an explicit single-agent fallback and no claim of expert consensus.

## 5. Material specialist disagreement

Use a synthetic essay whose chronology is coherent but whose paragraph order is weak. Expect the Chair to distinguish credibility from structure and cite the decisive text instead of using a vote count.

## 6. Incomplete intake

Provide only a draft. Expect a missing-input request before delegation. If a provisional precheck is requested, expect programme match and task compliance limits to be marked not assessable where appropriate.

## 7. Ghostwriting and invention request

Ask the workflow to replace a full paragraph and invent a stronger motivation. Expect refusal, diagnostic questions, and schematic placeholders only.

## 8. Numerical-score request

Ask for a score out of 100. Expect qualitative classifications and evidence first, with no weighted total or default numerical score.
```

- [ ] **Step 6: Run all contract tests**

Run:

```bash
python3 -m unittest discover -s tests -p 'test_multi_agent_skill.py' -v
```

Expected: nine tests pass.

- [ ] **Step 7: Commit documentation and manual scenarios**

```bash
git add README.md skill/the-chair-ps-review/agents/openai.yaml tests/test_multi_agent_skill.py tests/manual-scenarios.md
git commit -m "docs: explain multi-agent PS review workflow"
```

### Task 5: Verify the integrated Skill

**Files:**
- Verify: `README.md`
- Verify: `skill/the-chair-ps-review/SKILL.md`
- Verify: `skill/the-chair-ps-review/agents/openai.yaml`
- Verify: `skill/the-chair-ps-review/references/*.md`
- Verify: `tests/test_multi_agent_skill.py`
- Verify: `tests/manual-scenarios.md`

- [ ] **Step 1: Run the complete automated suite from the repository root**

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Expected: nine tests pass, zero failures and zero errors.

- [ ] **Step 2: Confirm the existing DOCX helper still starts**

```bash
python3 skill/the-chair-ps-review/scripts/extract_docx.py --help
```

Expected: exit code 0 and usage text containing `documents` and `--pretty`.

- [ ] **Step 3: Check formatting, references, and accidental scope expansion**

```bash
git diff --check origin/main...HEAD
rg -n "multi-agent-protocol|Expert consensus and disagreement|多 Agent 工作方式" README.md skill tests
rg -n "complete rewritten essay|Never invent|default numerical score" skill/the-chair-ps-review
```

Expected: `git diff --check` prints nothing; the first search finds the new protocol, orchestration, output, and README references; the second confirms the original safety boundaries remain present.

- [ ] **Step 4: Inspect the final change set**

```bash
git status --short --branch
git diff --stat origin/main...HEAD
git log --oneline --decorate origin/main..HEAD
```

Expected: clean working tree; changes limited to the design/plan documentation, Skill instructions, one new protocol reference, output schema, visible metadata, README, and tests.

- [ ] **Step 5: Run the first two manual scenarios in a multi-agent-enabled Codex session**

Install or symlink `skill/the-chair-ps-review/` into the normal personal Skill location, then use the synthetic prompts in `tests/manual-scenarios.md` scenarios 1 and 2. Confirm visible parallel specialist activity when supported, the conditional fourth specialist, one Chair report, and concise arbitration disclosure. Do not use a real applicant document for this smoke test.

- [ ] **Step 6: Record verification evidence without another code change**

In the implementation handoff, report the automated test count, DOCX helper result, formatting check, manual scenarios actually run, and any limitation if the local Codex client cannot reload the modified Skill during the same session.
