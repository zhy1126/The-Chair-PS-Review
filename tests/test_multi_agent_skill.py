"""Static instruction-contract checks; runtime behavior requires manual scenarios."""

from pathlib import Path
import re
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


def fenced_prompt(scenario: str) -> str:
    prompt_section = scenario[scenario.index("**Prompt**") : scenario.index("**Action**")]
    match = re.search(r"```text\n([\s\S]*?)\n```", prompt_section)
    if match is None:
        raise AssertionError("scenario is missing a fenced text prompt")
    return match.group(1)


ROLE_ENUM = (
    "`task-compliance`, `narrative-structure`, `depth-and-credibility`, "
    "`programme-match`"
)
STATUS_ENUM = "`completed`, `not_assessable`, `failed`"
PROVENANCE_ENUM = (
    "`not_applicable`, `pasted_user_supplied_official_text`, "
    "`verified_official_page`"
)
CONTRACT_FIELDS = (
    "role",
    "status",
    "source_provenance",
    "scope_reviewed",
    "findings",
    "uncertainties",
    "overlap_flags",
)
STATUS_TRUTH_ROWS = (
    "| All requested roles | None | Normal multi-agent synthesis. |",
    "| At least one | At least one | Partial coverage: use only `completed` findings and disclose every non-completed dimension and status. |",
    "| Zero | All requested roles | Explicit single-agent fallback regardless of the `failed`/`not_assessable` mix; do not claim consensus. |",
)
CAPACITY_ROWS = (
    "| Fourth child slot available | Launch `programme-match` in the initial batch with the three fixed roles. |",
    "| Fourth child slot unavailable | Queue `programme-match` and start it at the earliest available slot; capacity queueing is not failure or reduced coverage. |",
)


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

    def test_protocol_defines_exact_enums_and_contract_fields(self) -> None:
        protocol = read(PROTOCOL)
        self.assertIn(f"Accepted role identifiers: {ROLE_ENUM}.", protocol)
        self.assertIn(f"Accepted statuses: {STATUS_ENUM}.", protocol)
        self.assertIn(f"Accepted source provenance values: {PROVENANCE_ENUM}.", protocol)
        contract = re.search(
            r"Return exactly one compact summary using this shape:\n\n```text\n([\s\S]*?)\n```",
            protocol,
        )
        self.assertIsNotNone(contract)
        assert contract is not None
        top_level_fields = re.findall(r"^([a-z_]+):", contract.group(1), re.MULTILINE)
        self.assertEqual(top_level_fields, list(CONTRACT_FIELDS))
        self.assertIn("source_provenance:", contract.group(1))

    def test_protocol_defines_status_invariants_and_malformed_normalization(self) -> None:
        protocol = read(PROTOCOL)
        for status_rule in (
            "`completed`: `findings` contains 0-5 entries; `uncertainties` may be `[]`; source provenance must be valid.",
            "`not_assessable`: `findings` must be `[]`; `uncertainties` must contain at least one missing-input reason; this is unavailable coverage and never evidence.",
            "`failed`: `findings` must be `[]`; `uncertainties` must contain one concise failure or invalid-response reason and no raw logs; this is failed coverage.",
            "All list fields must use the literal `[]` when empty.",
        ):
            self.assertIn(status_rule, protocol)
        for malformed_case in (
            "unknown role",
            "unknown status",
            "unknown source provenance",
            "missing or extra fields",
            "prose outside the contract",
            "more than five findings",
            "status-invariant violation",
        ):
            self.assertIn(malformed_case, protocol)
        self.assertIn("Normalize every malformed or missing response to `failed`", protocol)

    def test_protocol_has_exact_post_wait_truth_table(self) -> None:
        protocol = read(PROTOCOL)
        for row in STATUS_TRUTH_ROWS:
            self.assertIn(row, protocol)

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
        self.assertIn("Launch the three fixed specialists concurrently", chair)
        self.assertIn("Wait for every requested role before synthesis", chair)
        self.assertIn(
            "resolve them by direct draft evidence, source-labelled programme material, role ownership, and the qualitative rubric",
            chair,
        )
        self.assertIn("Consensus is supporting evidence, not a vote", chair)

    def test_protocol_capacity_safe_scheduling_requests_and_waits_for_every_role(self) -> None:
        protocol = read(PROTOCOL)
        chair = section(protocol, "## Chair arbitration")
        self.assertIn("Request every applicable role", chair)
        self.assertIn("Launch the three fixed specialists concurrently", chair)
        for row in CAPACITY_ROWS:
            self.assertIn(row, chair)
        self.assertIn("Wait for every requested role before synthesis", chair)
        self.assertNotIn("same batch only", chair)

    def test_protocol_preserves_programme_source_provenance(self) -> None:
        protocol = read(PROTOCOL)
        programme = section(protocol, "## Programme-match specialist")
        self.assertIn("`pasted_user_supplied_official_text`", programme)
        self.assertIn("must never be described as independently verified", programme)
        self.assertIn("`verified_official_page`", programme)
        self.assertIn("Retain `source_provenance`", programme)

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
        self.assertIn("Request every applicable specialist role", skill)
        self.assertIn("Wait for every requested specialist", skill)
        self.assertIn("The primary agent remains the Chair", skill)

    def test_skill_uses_capacity_safe_scheduling(self) -> None:
        skill = read(SKILL)
        self.assertIn("Launch the three fixed roles concurrently", skill)
        for row in CAPACITY_ROWS:
            self.assertIn(row, skill)
        self.assertIn("Capacity queueing is not failure or reduced coverage", skill)

    def test_skill_uses_conditional_programme_specialist_and_explicit_fallback(self) -> None:
        skill = read(SKILL)
        self.assertIn("Do not launch the programme-match specialist", skill)
        self.assertIn("official programme information", skill)
        self.assertIn("tell the user before falling back", skill.lower())
        self.assertIn("Never claim expert consensus after a full fallback", skill)
        self.assertIn(
            "If at least one normalized result is `completed` and at least one is non-completed",
            skill,
        )
        self.assertIn(
            "preserve only the completed findings and disclose every non-completed dimension and status",
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
            "programme-match gets only draft match claims, training needs, source-labelled verified/pasted official programme information, and its `source_provenance`",
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
        self.assertIn("If zero normalized results are `completed`", skill)
        self.assertIn("Never carry full specialist reports or private reasoning into Chair synthesis", skill)

    def test_skill_defines_exact_normalization_contract_and_truth_table(self) -> None:
        skill = read(SKILL)
        self.assertIn(f"Accepted role identifiers: {ROLE_ENUM}.", skill)
        self.assertIn(f"Accepted statuses: {STATUS_ENUM}.", skill)
        self.assertIn(f"Accepted source provenance values: {PROVENANCE_ENUM}.", skill)
        self.assertIn("exactly these seven fields", skill)
        self.assertIn(", ".join(f"`{field}`" for field in CONTRACT_FIELDS), skill)
        self.assertIn("Normalize every malformed or missing response to `failed`", skill)
        for invariant in (
            "`completed` permits 0-5 findings",
            "`not_assessable` requires `findings: []`",
            "`failed` requires `findings: []`",
            "All list fields use the literal `[]` when empty.",
        ):
            self.assertIn(invariant, skill)
        for malformed_case in (
            "Unknown role, status, or provenance",
            "missing or extra fields",
            "prose outside the contract",
            "more than five findings",
            "status-invariant violation",
        ):
            self.assertIn(malformed_case, skill)
        for row in STATUS_TRUTH_ROWS:
            self.assertIn(row, skill)

    def test_skill_labels_and_retains_programme_source_provenance(self) -> None:
        skill = read(SKILL)
        self.assertIn("Before launching `programme-match`, label its programme source", skill)
        self.assertIn("`pasted_user_supplied_official_text`", skill)
        self.assertIn("`verified_official_page`", skill)
        self.assertIn("must never be called independently verified", skill)
        self.assertIn("retain `source_provenance` through final programme claims and arbitration", skill)

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

    def test_output_schema_is_section_scoped_for_partial_and_zero_completed_results(self) -> None:
        transparency = section(read(OUTPUT_SCHEMA), "## 12. Expert consensus and disagreement")
        for row in STATUS_TRUTH_ROWS:
            self.assertIn(row, transparency)
        self.assertIn(
            "at least one `completed` and at least one non-completed role",
            transparency,
        )
        self.assertIn("use findings only from `completed` roles", transparency)
        self.assertIn("name every non-completed dimension and status", transparency)
        self.assertIn("zero `completed` roles", transparency)
        self.assertIn("single-agent fallback", transparency)
        self.assertIn("regardless of the `failed`/`not_assessable` mix", transparency)
        zero_completed = transparency[transparency.index("zero `completed` roles") :]
        self.assertNotIn("preserve successful", zero_completed.lower())


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

    def test_readme_distinguishes_pasted_material_from_independent_verification(self) -> None:
        readme = read(README)
        self.assertIn("用户粘贴的官方资料", readme)
        self.assertIn("仅据该材料检查文书主张", readme)
        self.assertIn("不能称为独立核验", readme)
        self.assertIn("成功访问官方页面", readme)
        self.assertIn("独立核验", readme)

    def test_readme_documents_capacity_queue_and_static_test_scope(self) -> None:
        readme = read(README)
        self.assertIn("前三个固定专家并发启动", readme)
        self.assertIn("最早可用名额", readme)
        self.assertIn("排队不算失败或覆盖降级", readme)
        self.assertIn("自动化测试仅做静态指令契约校验", readme)
        self.assertIn("运行时行为仍需手工场景", readme)

    def test_readme_numbered_output_punctuation(self) -> None:
        output = section(read(README), "## 输出内容")
        numbered = re.findall(r"^(\d+)\. (.+)$", output, re.MULTILINE)
        self.assertEqual([int(number) for number, _ in numbered], list(range(1, 13)))
        for number, item in numbered[:-1]:
            self.assertTrue(item.endswith("；"), f"README item {number} must end with a semicolon")
        self.assertTrue(numbered[-1][1].endswith("。"), "README item 12 must end with a period")

    def test_visible_metadata_mentions_parallel_expert_review(self) -> None:
        lines = read(OPENAI_YAML).splitlines()
        self.assertEqual(lines[0], "interface:")
        self.assertEqual(len(lines), 4)
        fields = {}
        for line in lines[1:]:
            match = re.fullmatch(
                r'  (display_name|short_description|default_prompt): "([^"]+)"', line
            )
            self.assertIsNotNone(match, f"invalid interface field: {line}")
            assert match is not None
            fields[match.group(1)] = match.group(2)
        self.assertEqual(
            set(fields), {"display_name", "short_description", "default_prompt"}
        )
        self.assertIn("多专家并行", fields["short_description"])
        self.assertIn("由 Chair 仲裁", fields["short_description"])
        self.assertGreaterEqual(len(fields["short_description"]), 25)
        self.assertLessEqual(len(fields["short_description"]), 64)
        self.assertIn("多 Agent", fields["display_name"])
        self.assertIn("多专家并行", fields["default_prompt"])
        self.assertIn("由 Chair 仲裁", fields["default_prompt"])

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

    def test_manual_scenarios_document_copy_paste_runtime_checks(self) -> None:
        scenarios = read(MANUAL_SCENARIOS)
        self.assertIn("# Multi-Agent Runtime Manual Scenarios", scenarios)
        self.assertIn("copy-paste runtime checks", scenarios)
        self.assertIn("## Synthetic fixture", scenarios)
        fixture = section(scenarios, "## Synthetic fixture")
        for detail in (
            "Applicant background",
            "Exact essay prompt",
            "Word limit",
            "Synthetic official programme information",
            "Paragraph 1",
            "Paragraph 2",
            "Paragraph 3",
            "Paragraph 4",
        ):
            self.assertIn(detail, fixture)

        for number, title in (
            (1, "Complete four-specialist review"),
            (2, "Three-specialist review without official programme information"),
            (3, "Partial specialist failure"),
            (4, "Total specialist failure"),
            (5, "Material specialist disagreement"),
            (6, "Incomplete intake"),
            (7, "Ghostwriting and invention request"),
            (8, "Numerical-score request"),
        ):
            scenario = section(scenarios, f"## {number}. {title}")
            for marker in ("**Setup**", "**Prompt**", "**Action**", "**Pass criteria**"):
                self.assertIn(marker, scenario)
            prompt = scenario[scenario.index("**Prompt**") : scenario.index("**Action**")]
            self.assertRegex(prompt, r"```text\n[\s\S]*\$the-chair-ps-review[\s\S]*\n```")

    def test_full_review_scenario_prompts_include_complete_intake(self) -> None:
        scenarios = read(MANUAL_SCENARIOS)
        titles = {
            1: "Complete four-specialist review",
            2: "Three-specialist review without official programme information",
            3: "Partial specialist failure",
            4: "Total specialist failure",
            5: "Material specialist disagreement",
            7: "Ghostwriting and invention request",
            8: "Numerical-score request",
        }
        mandatory = (
            "Application category:",
            "Essay type:",
            "Exact institution/programme:",
            "Official essay prompt:",
            "Word limit:",
            "Draft:",
        )
        for number, title in titles.items():
            prompt = fenced_prompt(section(scenarios, f"## {number}. {title}"))
            for label in mandatory:
                self.assertIn(label, prompt, f"scenario {number} missing {label}")
            if number != 2:
                self.assertIn(
                    "Pasted official programme information:",
                    prompt,
                    f"scenario {number} must provide programme-match evidence",
                )

        scenario_2 = fenced_prompt(
            section(scenarios, "## 2. Three-specialist review without official programme information")
        )
        self.assertIn("provisional precheck", scenario_2.lower())
        self.assertIn("Official programme information: withheld", scenario_2)

        scenario_6 = section(scenarios, "## 6. Incomplete intake")
        self.assertIn("intentionally incomplete", scenario_6.lower())
        self.assertIn("asks for missing inputs before delegation", scenario_6)

    def test_failure_and_disagreement_scenarios_state_runtime_prerequisites(self) -> None:
        scenarios = read(MANUAL_SCENARIOS)
        for number, title in (
            (3, "Partial specialist failure"),
            (4, "Total specialist failure"),
        ):
            scenario = section(scenarios, f"## {number}. {title}")
            for marker in (
                "**Prerequisite**",
                "Codex client/harness",
                "visible Subagents controls",
                "stop/interrupt",
                "If unavailable",
                "`SKIPPED`",
            ):
                self.assertIn(marker, scenario)

        disagreement = section(scenarios, "## 5. Material specialist disagreement")
        for marker in (
            "**Prerequisite**",
            "steer/inject seeded synthetic compact specialist results",
            "`INCONCLUSIVE/SKIPPED`",
            "must not fabricate disagreement",
        ):
            self.assertIn(marker, disagreement)

    def test_complete_review_scenario_allows_capacity_queueing(self) -> None:
        scenario = section(read(MANUAL_SCENARIOS), "## 1. Complete four-specialist review")
        self.assertIn("four visible specialists at once", scenario)
        self.assertIn("three active specialists plus `programme-match` queued", scenario)
        self.assertIn("earliest available slot", scenario)

    def test_touched_documentation_uses_lf_line_endings(self) -> None:
        for path in (README, OPENAI_YAML):
            self.assertNotIn(b"\r\n", path.read_bytes(), f"CRLF found in {path}")


if __name__ == "__main__":
    unittest.main()
