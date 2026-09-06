"""Static instruction contracts and local review-package checks; no model calls.

Run: python3 -m unittest discover -s skills/tracer/tracer-autopilot/tests -v
These checks catch document drift, not whether a model will obey the workflow.
"""
from pathlib import Path
import re
import subprocess
import tempfile
import unittest

AUTOPILOT = Path(__file__).resolve().parents[1]
TRACER = AUTOPILOT.parent
REPO = TRACER.parents[1]


def read(path):
    return path.read_text()


class InstructionContractTests(unittest.TestCase):
    def test_delivery_wide_budget_and_resume_accounting(self):
        skill = read(AUTOPILOT / "SKILL.md")
        for required in [
            "two review rounds and at most one consolidated repair pass",
            "not that allowance per task, reviewer, or axis",
            "no independent review gates",
            "No third review, second repair pass",
            "generic “continue” does not reset it",
            "Workflow: autopilot-bounded-v1",
            "Round 1: not-started | running | complete",
            "Round 2: not-started | running | complete",
            "legacy ledger without review accounting",
            "Mark a phase running **before** dispatch",
        ]:
            with self.subTest(required=required):
                self.assertIn(required, skill)
        inline = skill.split("## Inline mode", 1)[1]
        self.assertIn("two-round budget, one repair pass", inline)

    def test_round_two_uses_correction_delta_and_preserves_blockers(self):
        skill = read(AUTOPILOT / "SKILL.md")
        closing = skill.split("## Phase 4", 1)[1].split("## Phase 5", 1)[0]
        self.assertIn('scripts/review-package "$FIX_BASE" "$FINAL_HEAD"', closing)
        self.assertNotIn('scripts/review-package "$BASE"', closing)
        self.assertIn("empty correction diff is valid", closing)
        self.assertIn("no implementation repair follows round 2", closing)
        self.assertIn("Newly demonstrated defects remain visible", closing)
        prompt = read(AUTOPILOT / "closing-verifier-prompt.md")
        for required in ["do not restart", "No nested review or fixer runs",
                         "proven/disproven/unverified", "Preserve tracked files, index, and HEAD"]:
            self.assertIn(required, prompt)

    def test_no_task_review_or_nested_repair_template(self):
        self.assertFalse((AUTOPILOT / "task-reviewer-prompt.md").exists())
        skill = read(AUTOPILOT / "SKILL.md")
        implementation = skill.split("## Phase 2", 1)[1].split("## Phase 3", 1)[0]
        self.assertNotIn("reviewer-prompt.md", implementation)
        self.assertIn("focused TDD checks and one self-check", implementation)
        for prompt in AUTOPILOT.glob("*-prompt.md"):
            with self.subTest(prompt=prompt.name):
                self.assertNotRegex(read(prompt), r"(?i)loop until|re-review until|after every task")
        fixer = read(AUTOPILOT / "fixer-prompt.md")
        self.assertIn("all\n       affected consumers", fixer)
        self.assertIn("Preserve every accepted invariant", fixer)

    def test_shared_protocols_keep_user_only_entry_points(self):
        for name, reference in [
            ("tracer-convince-me", "proof-protocol.md"),
            ("tracer-finish-branch", "branch-finishing.md"),
        ]:
            entry = read(TRACER / name / "SKILL.md")
            self.assertIn("disable-model-invocation: true", entry)
            self.assertIn(f"]({reference})", entry)
            self.assertIn(f"](../{name}/{reference})", read(AUTOPILOT / "SKILL.md"))
        proof = read(TRACER / "tracer-convince-me/proof-protocol.md")
        self.assertIn("does not authorize implementation repairs or further review rounds", proof)
        for section in proof.split("## ")[1:]:
            with self.subTest(section=section.splitlines()[0]):
                self.assertIn("**Complete when:**", section)
        self.assertIn("Get approval before destructive actions", proof)
        self.assertIn("Do not weaken the proof", proof)

    def test_outcomes_and_finishing_do_not_reopen_budget(self):
        skill = read(AUTOPILOT / "SKILL.md")
        outcomes = skill.split("## Phase 5", 1)[1].split("## Inline mode", 1)[0]
        for state in ["**Complete:**", "**Complete with follow-ups:**", "**Blocked:**"]:
            self.assertIn(state, outcomes)
        self.assertIn("Stop without merge, push, PR, discard, or cleanup", outcomes)
        finish = read(TRACER / "tracer-finish-branch/branch-finishing.md")
        for required in ["same unchanged HEAD and tracked tree", "required acceptance remains blocked/unverified",
                         "Wait for the user's explicit choice", "verify tests on the merged result",
                         "Type 'discard' to confirm", "Only remove worktrees this workflow created"]:
            self.assertIn(required, finish)
        review = read(TRACER / "tracer-code-review/SKILL.md")
        self.assertIn("**Workflow-owned review:** return after step 5", review)

    def test_changed_document_links_resolve(self):
        docs = list(AUTOPILOT.glob("*.md")) + [
            TRACER / "README.md", REPO / "README.md",
            TRACER / "tracer-wat/SKILL.md",
            TRACER / "tracer-code-review/SKILL.md",
            TRACER / "tracer-convince-me/SKILL.md",
            TRACER / "tracer-convince-me/proof-protocol.md",
            TRACER / "tracer-finish-branch/SKILL.md",
            TRACER / "tracer-finish-branch/branch-finishing.md",
        ]
        for doc in docs:
            for link in re.findall(r"\]\(([^)]+)\)", read(doc)):
                if "://" in link or link.startswith("#"):
                    continue
                with self.subTest(doc=str(doc), link=link):
                    self.assertTrue((doc.parent / link.split("#", 1)[0]).exists())


class ReviewPackageTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.addCleanup(self.tmp.cleanup)
        self.git("init", "-q")
        self.git("config", "user.name", "Fixture")
        self.git("config", "user.email", "fixture@example.invalid")
        self.git("config", "commit.gpgsign", "false")
        self.git("config", "core.hooksPath", "/dev/null")
        self.base = self.commit("baseline.txt", "baseline\n", "Add fixture baseline")
        self.review_head = self.commit("feature.txt", "feature-before-repair\n", "Add fixture behavior")
        self.final_head = self.commit("feature.txt", "feature-after-repair\n", "Correct fixture behavior")

    def git(self, *args):
        return subprocess.run(["git", *args], cwd=self.root, check=True,
                              capture_output=True, text=True).stdout.strip()

    def commit(self, filename, content, message):
        (self.root / filename).write_text(content)
        self.git("add", filename)
        self.git("commit", "-qm", message)
        return self.git("rev-parse", "HEAD")

    def package(self, base, head):
        output = self.root / "review.diff"
        subprocess.run(["bash", str(AUTOPILOT / "scripts/review-package"), base, head, str(output)],
                       cwd=self.root, check=True, capture_output=True, text=True)
        return output.read_text()

    def test_round_two_contains_only_correction_not_initial_delivery(self):
        broad = self.package(self.base, self.review_head)
        focused = self.package(self.review_head, self.final_head)
        self.assertIn("Add fixture behavior", broad)
        self.assertIn("Correct fixture behavior", focused)
        self.assertNotIn("Add fixture behavior", focused)
        self.assertIn("-feature-before-repair", focused)
        self.assertIn("+feature-after-repair", focused)

    def test_skipped_repair_accepts_empty_delta(self):
        package = self.package(self.review_head, self.review_head)
        self.assertIn("## Diff", package)
        self.assertNotIn("diff --git", package)


if __name__ == "__main__":
    unittest.main()
