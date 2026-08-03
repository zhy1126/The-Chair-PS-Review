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
