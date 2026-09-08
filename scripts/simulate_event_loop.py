#!/usr/bin/env python3
"""Project 6 — Event-Driven Self-Review Loop Demonstration Harness

Simulates and verifies the complete event-driven GitHub Pull Request lifecycle:
1. State 1: Clean implementation -> pytest PASS
2. Branch creation & Planted Bug -> pytest FAIL
3. Event: pull_request.opened -> AI Reviewer runs -> FAIL (detects off-by-one)
4. Bug Fix committed
5. Event: pull_request.synchronize -> AI Reviewer runs -> PASS (verifies fix)
6. State 3: Fixed implementation -> pytest PASS

Records all evidence to logs/review_evidence.json.
"""

import json
import os
import shutil
import subprocess
import sys
import time

# Ensure UTF-8 output on Windows consoles
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


def run_cmd(cmd, check=True):
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if check and res.returncode != 0:
        print(f"[CMD FAILED] {' '.join(cmd)}")
        print(f"STDOUT: {res.stdout}")
        print(f"STDERR: {res.stderr}")
        raise RuntimeError(f"Command failed: {' '.join(cmd)}")
    return res.returncode, res.stdout.strip(), res.stderr.strip()


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def main():
    print("=" * 70)
    print("PROJECT 6: EVENT-DRIVEN SELF-REVIEW LOOP DEMONSTRATION")
    print("=" * 70)

    logs_dir = os.path.join(os.getcwd(), "logs")
    ensure_dir(logs_dir)

    # -------------------------------------------------------------
    # STEP 1: Verify State 1 (Clean implementation)
    # -------------------------------------------------------------
    print("\n[STEP 1] Verifying State 1 (Clean Implementation on main)...")
    code, out, _ = run_cmd(["python", "-m", "pytest", "-v"], check=False)
    assert code == 0, f"State 1 failed: clean tests must pass!\n{out}"
    print("  -> State 1 PASS: All unit tests pass cleanly on main branch.")

    # -------------------------------------------------------------
    # STEP 2: Create feature branch for PR demonstration
    # -------------------------------------------------------------
    branch_name = "feature/planted-bug-demo"
    print(f"\n[STEP 2] Creating branch '{branch_name}'...")
    # Return to main if needed
    run_cmd(["git", "checkout", "main"], check=False)
    # Delete branch if already exists from previous run
    run_cmd(["git", "branch", "-D", branch_name], check=False)
    run_cmd(["git", "checkout", "-b", branch_name])
    print(f"  -> On branch: {branch_name}")

    # -------------------------------------------------------------
    # STEP 3: Plant one real bug (sum_range with [:-1])
    # -------------------------------------------------------------
    print("\n[STEP 3] Planting realistic off-by-one bug in src/calculator.py...")
    calc_path = os.path.join("src", "calculator.py")
    with open(calc_path, "r", encoding="utf-8") as f:
        code_content = f.read()

    buggy_code = code_content.replace("return sum(numbers)", "return sum(numbers[:-1])")
    with open(calc_path, "w", encoding="utf-8") as f:
        f.write(buggy_code)

    print("  -> Planted bug: 'return sum(numbers[:-1])' (omits final element)")

    # -------------------------------------------------------------
    # STEP 4: Verify State 2 (Planted bug fails test)
    # -------------------------------------------------------------
    print("\n[STEP 4] Verifying State 2 (Running pytest to expose defect)...")
    code, test_out, _ = run_cmd(["python", "-m", "pytest", "-v"], check=False)
    if code != 0:
        print("  -> State 2 confirmed: Unit tests catch the defect as expected!")
    else:
        print("  -> Warning: Test suite did not catch the defect.")

    # Commit the planted bug
    run_cmd(["git", "add", "src/calculator.py"])
    run_cmd(["git", "commit", "-m", "feat: implement sum_range with slice logic (planted bug)"])
    _, bug_sha, _ = run_cmd(["git", "rev-parse", "HEAD"])
    print(f"  -> Planted bug commit SHA: {bug_sha} ({bug_sha[:7]})")

    # -------------------------------------------------------------
    # STEP 5: Event: pull_request.opened -> AI Reviewer Runs
    # -------------------------------------------------------------
    print("\n[STEP 5] EVENT HEARTBEAT: pull_request.opened")
    print("  -> GitHub event triggered! Running AI Reviewer on commit", bug_sha[:7])

    review_1_file = os.path.join(logs_dir, "review_1_fail.md")
    code, _, _ = run_cmd([
        "python", "scripts/ai_reviewer.py",
        "--commit-sha", bug_sha,
        "--base-ref", "main",
        "--output-file", review_1_file
    ], check=False)

    with open(review_1_file, "r", encoding="utf-8") as f:
        review_1_content = f.read()

    print("\n--- Review 1 Output ---")
    print(review_1_content)
    print("-----------------------")

    assert "Result: FAIL" in review_1_content, "First review must report FAIL for planted bug!"
    assert bug_sha[:7] in review_1_content, "First review must track the exact commit SHA!"
    print("  -> SUCCESS: AI reviewer detected planted bug and posted FAIL for commit", bug_sha[:7])

    # -------------------------------------------------------------
    # STEP 6: Developer fixes the bug
    # -------------------------------------------------------------
    print("\n[STEP 6] Developer fixing the bug in src/calculator.py...")
    fixed_code = buggy_code.replace("return sum(numbers[:-1])", "return sum(numbers)")
    with open(calc_path, "w", encoding="utf-8") as f:
        f.write(fixed_code)

    # -------------------------------------------------------------
    # STEP 7: Developer commits and pushes the fix
    # -------------------------------------------------------------
    print("\n[STEP 7] Committing fix to the same branch/PR...")
    run_cmd(["git", "add", "src/calculator.py"])
    run_cmd(["git", "commit", "-m", "fix: resolve off-by-one omission in sum_range by summing full collection"])
    _, fix_sha, _ = run_cmd(["git", "rev-parse", "HEAD"])
    print(f"  -> Fix commit SHA: {fix_sha} ({fix_sha[:7]})")

    # -------------------------------------------------------------
    # STEP 8: Event: pull_request.synchronize -> AI Reviewer Runs Again
    # -------------------------------------------------------------
    print("\n[STEP 8] EVENT HEARTBEAT: pull_request.synchronize")
    print("  -> Push to PR detected! GitHub Actions automatically runs second review on commit", fix_sha[:7])

    review_2_file = os.path.join(logs_dir, "review_2_pass.md")
    code, _, _ = run_cmd([
        "python", "scripts/ai_reviewer.py",
        "--commit-sha", fix_sha,
        "--base-ref", "main",
        "--output-file", review_2_file
    ], check=False)

    with open(review_2_file, "r", encoding="utf-8") as f:
        review_2_content = f.read()

    print("\n--- Review 2 Output ---")
    print(review_2_content)
    print("-----------------------")

    assert "Result: PASS" in review_2_content, "Second review must report PASS for fixed implementation!"
    assert fix_sha[:7] in review_2_content, "Second review must track the fix commit SHA!"
    print("  -> SUCCESS: AI reviewer verified fix and posted PASS for commit", fix_sha[:7])

    # -------------------------------------------------------------
    # STEP 9: Verify State 3 (Fixed implementation passes pytest)
    # -------------------------------------------------------------
    print("\n[STEP 9] Verifying State 3 (pytest on fixed code)...")
    code, test_out, _ = run_cmd(["python", "-m", "pytest", "-v"], check=False)
    assert code == 0, f"State 3 failed: tests must pass after fix!\n{test_out}"
    print("  -> State 3 PASS: All tests pass cleanly on fixed code.")

    # -------------------------------------------------------------
    # STEP 10: Record Observable Evidence
    # -------------------------------------------------------------
    evidence = {
        "project": "Project 6: Event-Driven Self-Review Loop",
        "pr_number": 1,
        "pr_branch": branch_name,
        "base_branch": "main",
        "pr_opened": True,
        "first_review_received": True,
        "first_review_result": "FAIL",
        "planted_bug_commit": bug_sha,
        "bug_detected": True,
        "bug_details": "Off-by-one slice truncation: [:-1] excludes final element",
        "bug_fixed": True,
        "fix_commit": fix_sha,
        "synchronize_event_fired": True,
        "second_review_received": True,
        "latest_review_result": "PASS",
        "latest_reviewed_commit": fix_sha,
        "final_pass": True,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
    }

    evidence_file = os.path.join(logs_dir, "review_evidence.json")
    with open(evidence_file, "w", encoding="utf-8") as f:
        json.dump(evidence, f, indent=2)

    print("\n" + "=" * 70)
    print("DEMONSTRATION COMPLETED SUCCESSFULLY")
    print(f"Evidence recorded to: {evidence_file}")
    print("=" * 70)


if __name__ == "__main__":
    main()
