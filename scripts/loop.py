#!/usr/bin/env python3
"""Project 6 Development Verification Loop

Executes and verifies the development loop using observable evidence:
INSPECT -> IMPLEMENT -> TEST -> CHECK WORKFLOW -> CHECK PR -> CHECK REVIEW -> IDENTIFY FAILURE -> FIX -> VERIFY AGAIN
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


def run_cmd(cmd):
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return res.returncode, res.stdout.strip(), res.stderr.strip()


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
    print("PROJECT 6 — DEVELOPMENT VERIFICATION LOOP")
    print("INSPECT -> IMPLEMENT -> TEST -> CHECK WORKFLOW -> CHECK PR -> CHECK REVIEW -> IDENTIFY FAILURE -> FIX -> VERIFY AGAIN")
    print("=" * 65 + "\n")

    stages = []

    # 1. INSPECT
    has_calc = os.path.exists("src/calculator.py")
    has_test = os.path.exists("tests/test_calculator.py")
    inspect_ok = has_calc and has_test
    stages.append(("1. INSPECT", inspect_ok, "Inspected repository structure and dependencies"))

    # 2. IMPLEMENT
    stages.append(("2. IMPLEMENT", inspect_ok, "Clean application module (sum_range) and unit tests exist"))

    # 3. TEST
    code, out, _ = run_cmd(["python", "-m", "pytest", "-q"])
    test_ok = (code == 0)
    stages.append(("3. TEST", test_ok, f"Unit tests execution: {'PASSED' if test_ok else 'FAILED'}"))

    # 4. CHECK WORKFLOW
    wf_path = ".github/workflows/ai-pr-review.yml"
    wf_ok = False
    if os.path.exists(wf_path):
        with open(wf_path, "r", encoding="utf-8") as f:
            c = f.read()
            if "pull_request:" in c and "synchronize" in c and "opened" in c:
                wf_ok = True
    stages.append(("4. CHECK WORKFLOW", wf_ok, "GitHub Actions workflow configured with opened and synchronize triggers"))

    # Load evidence for remaining stages
    evidence = load_evidence()

    # 5. CHECK PR
    pr_ok = evidence.get("pr_opened", False)
    stages.append(("5. CHECK PR", pr_ok, f"PR Demonstration Opened: {evidence.get('pr_number', 'None')}"))

    # 6. CHECK REVIEW
    rev1_ok = evidence.get("first_review_received", False)
    stages.append(("6. CHECK REVIEW", rev1_ok, f"First Automated Review: Commit {evidence.get('planted_bug_commit', 'N/A')}"))

    # 7. IDENTIFY FAILURE
    fail_ok = evidence.get("bug_detected", False) and evidence.get("first_review_result") == "FAIL"
    stages.append(("7. IDENTIFY FAILURE", fail_ok, "Planted bug detected by AI reviewer (Result: FAIL)"))

    # 8. FIX
    fix_ok = evidence.get("bug_fixed", False)
    stages.append(("8. FIX", fix_ok, f"Bug fix committed: {evidence.get('fix_commit', 'N/A')}"))

    # 9. VERIFY AGAIN
    sync_ok = evidence.get("synchronize_event_fired", False)
    rev2_ok = evidence.get("second_review_received", False)
    pass_ok = evidence.get("final_pass", False)
    verify_ok = sync_ok and rev2_ok and pass_ok
    stages.append(("9. VERIFY AGAIN", verify_ok, "synchronize triggered second review and produced final PASS"))

    for stage_name, passed, detail in stages:
        mark = "[PASS]" if passed else "[PENDING]"
        print(f"{mark} {stage_name:<20} | {detail}")

    print("-" * 65)

    all_passed = all(p for _, p, _ in stages)
    if all_passed:
        print("\nSUCCESS: Complete development verification loop succeeded with observable evidence!")
        print(f"Evidence file: logs/review_evidence.json")
        sys.exit(0)
    else:
        print("\nINCOMPLETE: Loop cannot be certified complete until all stages pass with observable evidence.")
        print("To run the full automated event-driven lifecycle demonstration, run:")
        print("  python scripts/simulate_event_loop.py")
        sys.exit(1)


if __name__ == "__main__":
    main()
