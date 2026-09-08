#!/usr/bin/env python3
"""Project 6 Goal Command

Audits repository status, validates requirements against observable evidence,
and reports the current completion state.
"""

import json
import os
import subprocess
import sys

# Ensure UTF-8 output on Windows consoles
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


def check_file(path: str) -> bool:
    return os.path.exists(path)


def load_evidence() -> dict:
    evidence_path = os.path.join("logs", "review_evidence.json")
    if os.path.exists(evidence_path):
        try:
            with open(evidence_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def main():
    print("=" * 65)
    print("PROJECT 6 GOAL\n")
    print("Build an event-driven GitHub Pull Request self-review loop.\n")
    print("Success requires:")
    print("- automatic PR review")
    print("- planted bug detection")
    print("- bug fix")
    print("- synchronize-triggered second review")
    print("- final PASS")
    print("=" * 65 + "\n")

    evidence = load_evidence()

    # Checklist evaluations based on verifiable artifacts & evidence
    checks = [
        ("Python application exists (src/calculator.py)", check_file("src/calculator.py")),
        ("Test suite exists (tests/test_calculator.py)", check_file("tests/test_calculator.py")),
        ("GitHub workflow exists (.github/workflows/ai-pr-review.yml)", check_file(".github/workflows/ai-pr-review.yml")),
        ("Workflow triggers on pull_request opened, synchronize, reopened", False),
        ("AI Reviewer configured (scripts/ai_reviewer.py)", check_file("scripts/ai_reviewer.py")),
        ("Antigravity /goal command ready", check_file("scripts/goal.py") and check_file(".agents/skills/goal/SKILL.md")),
        ("Antigravity /loop command ready", check_file("scripts/loop.py") and check_file(".agents/skills/loop/SKILL.md")),
        ("Antigravity /schedule command ready", check_file("scripts/schedule.py") and check_file(".agents/skills/schedule/SKILL.md")),
        ("Documentation & Progress (progress.md, README.md)", check_file("progress.md") and check_file("README.md")),
        ("PR Opened / Demonstration Initialized", evidence.get("pr_opened", False)),
        ("First automatic review received", evidence.get("first_review_received", False)),
        ("Planted off-by-one bug detected (Result: FAIL)", evidence.get("bug_detected", False)),
        ("Bug fix committed and pushed", evidence.get("bug_fixed", False)),
        ("synchronize event triggered", evidence.get("synchronize_event_fired", False)),
        ("Second automatic review received", evidence.get("second_review_received", False)),
        ("Final PASS confirmed", evidence.get("final_pass", False)),
    ]

    # Verify workflow triggers
    wf_path = ".github/workflows/ai-pr-review.yml"
    if os.path.exists(wf_path):
        with open(wf_path, "r", encoding="utf-8") as f:
            content = f.read()
            if "pull_request:" in content and "opened" in content and "synchronize" in content:
                # Update index 3
                checks[3] = ("Workflow triggers on pull_request opened, synchronize, reopened", True)

    completed = []
    missing = []

    for name, ok in checks:
        if ok:
            completed.append(name)
        else:
            missing.append(name)

    print(f"Implementation Status Audit ({len(completed)}/{len(checks)} Verified):")
    print("-" * 50)
    for item in completed:
        print(f"  [x] {item}")
    for item in missing:
        print(f"  [ ] {item}")

    print("\n" + "=" * 50)
    if evidence.get("final_pass"):
        print("STATUS: PASS - All Project 6 event-driven criteria verified with observable evidence!")
        print(f"Reviewed Commits:")
        print(f"  Initial Planted Bug Commit : {evidence.get('planted_bug_commit', 'N/A')} -> FAIL")
        print(f"  Synchronize Fix Commit     : {evidence.get('fix_commit', 'N/A')} -> PASS")
        sys.exit(0)
    else:
        print("STATUS: INCOMPLETE - Remaining requirements must be verified with observable evidence.")
        if missing:
            print("\nRemaining Work:")
            for item in missing:
                print(f"  - Execute and record evidence for: {item}")
        sys.exit(1)


if __name__ == "__main__":
    main()
