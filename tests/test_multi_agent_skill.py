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
        self.assertIn("If one or more, but not all, specialists fail", skill)
        self.assertIn(
            "preserve all successful results and disclose every dimension with reduced coverage",
            skill,
        )

    def test_skill_minimizes_context_for_each_specialist(self) -> None:
        skill = read(SKILL)
        self.assertIn("separately minimized packet for each specialist", skill)
        self.assertIn(
            "task-compliance gets prompt, limits, institution, programme, and draft but no irrelevant background",
            skill,
        )
        self.assertIn(
            "narrative gets draft plus only trajectory/background needed to understand progression",
            skill,
        )
        self.assertIn(
            "depth/credibility gets draft plus only chronology/role context needed",
            skill,
        )
        self.assertIn(
            "programme-match gets only draft match claims, training needs, and verified/pasted official programme information",
            skill,
        )
        self.assertIn("Do not send official programme material to roles that do not need it", skill)

    def test_skill_normalizes_specialist_results_before_synthesis(self) -> None:
        skill = read(SKILL)
        self.assertIn("Validate every returned summary against the shared result contract before synthesis", skill)
        self.assertIn("accept only known roles, valid statuses, required compact fields, and at most five findings", skill)
        self.assertIn("Retain only contract fields", skill)
        self.assertIn("Treat missing, malformed, or overlong responses as failed", skill)
        self.assertIn("valid `not_assessable` as unavailable coverage and never as evidence", skill)
        self.assertIn("Determine partial or total failure from normalized statuses", skill)
        self.assertIn("every launched response is failed, missing, or malformed", skill)
        self.assertIn("Never carry full specialist reports or private reasoning into Chair synthesis", skill)

    def test_skill_retains_existing_checklist_and_privacy_boundaries(self) -> None:
        skill = read(SKILL)
        self.assertIn("Do not perform a duplicate full review before launching specialists", skill)
        self.assertIn("Do not expose private chain-of-thought or append full specialist reports", skill)
        for heading in (
            "### 1. Classify the task",
            "### 2. Check hard requirements",
            "### 3. State the fit thesis",
            "### 4. Map the main line",
            "### 5. Audit CV-likeness",
            "### 6. Audit depth and credibility",
            "### 7. Audit programme match",
            "### 8. Classify after diagnosing",
            "### 9. Prioritise revision",
        ):
            self.assertIn(heading, skill)

class OutputTransparencyTests(unittest.TestCase):
    def test_output_schema_adds_concise_evidence_based_arbitration(self) -> None:
        schema = read(OUTPUT_SCHEMA)
        checklist = section(schema, "## 11. Self-revision checklist")
        transparency = section(schema, "## 12. Expert consensus and disagreement")
        self.assertLess(
            schema.index("## 11. Self-revision checklist"),
            schema.index("## 12. Expert consensus and disagreement"),
        )
        self.assertIn(
            "Include a concise checklist tailored to the draft before the final transparency section.",
            checklist,
        )
        self.assertNotIn("End with a concise checklist", checklist)
        self.assertIn("approximately 150 Chinese characters", transparency)
        self.assertIn("supported by more than one specialist", transparency)
        self.assertIn("competing conclusions", transparency)
        self.assertIn("evidence, not vote count", transparency)
        self.assertIn("Not assessable or reduced coverage", transparency)
        self.assertIn("failed specialist dimensions", transparency)
        self.assertIn("append complete specialist reports", transparency)
        self.assertIn("Do not expose private chain-of-thought", transparency)

    def test_output_schema_never_simulates_consensus_after_fallback(self) -> None:
        schema = read(OUTPUT_SCHEMA)
        transparency = section(schema, "## 12. Expert consensus and disagreement")
        skill = read(SKILL)
        self.assertIn("one-sentence fallback disclosure", transparency)
        self.assertIn("do not claim expert consensus", transparency)
        self.assertIn(
            "Include a self-revision checklist before the final expert consensus and disagreement section.",
            skill,
        )
        self.assertNotIn("End with a self-revision checklist.", skill)


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


if __name__ == "__main__":
    unittest.main()
