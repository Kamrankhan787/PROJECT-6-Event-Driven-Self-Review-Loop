#!/usr/bin/env python3
"""Project 6 Schedule Command — Monitoring and Recovery Watchdog

Audits PR review freshness, commit alignment, and failure states.
NOTE: This monitoring watchdog does NOT replace the event-driven heartbeat.
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
    print("PROJECT 6 SCHEDULE — MONITORING & RECOVERY WATCHDOG")
    print("-" * 65)
    print("Primary heartbeat : GitHub Pull Request event (opened / synchronize)")
    print("Monitoring/recovery: Schedule watchdog")
    print("=" * 65 + "\n")

    evidence = load_evidence()
    code, current_head, _ = run_cmd(["git", "rev-parse", "HEAD"])

    pr_open = evidence.get("pr_opened", False)
    latest_reviewed = evidence.get("latest_reviewed_commit")
    final_pass = evidence.get("final_pass", False)
    sync_fired = evidence.get("synchronize_event_fired", False)

    print("Watchdog Diagnostics:")
    print(f"  1. PR Active/Waiting for Review : {'YES (PR #' + str(evidence.get('pr_number', 1)) + ')' if pr_open else 'NO PR DETECTED'}")
    print(f"  2. Current Git HEAD             : {current_head[:10] if code == 0 else 'N/A'}")
    print(f"  3. Latest Reviewed Commit       : {latest_reviewed[:10] if latest_reviewed else 'NONE'}")
    
    # Check commit alignment / staleness
    if code == 0 and latest_reviewed:
        if current_head == latest_reviewed:
            staleness = "UP TO DATE (Latest commit has been reviewed)"
        else:
            staleness = f"STALE REVIEW (HEAD {current_head[:7]} != Reviewed {latest_reviewed[:7]})"
    elif not latest_reviewed:
        staleness = "PENDING (No reviews recorded yet)"
    else:
        staleness = "UNKNOWN"
    print(f"  4. Review Freshness Status      : {staleness}")

    # Check workflow status
    print(f"  5. synchronize Event Occurred   : {'YES' if sync_fired else 'NO'}")
    print(f"  6. Final Review Result          : {evidence.get('latest_review_result', 'PENDING')}")
    print(f"  7. Final PASS Status            : {'CONFIRMED (Ready to merge)' if final_pass else 'NOT REACHED'}")

    print("\nWatchdog Health Assessment:")
    if final_pass:
        print("  -> Healthy: Pull Request has completed the event-driven review loop and passed.")
    elif pr_open and not latest_reviewed:
        print("  -> Attention: PR is waiting for the initial event-driven review.")
    elif pr_open and current_head != latest_reviewed:
        print("  -> Recovery Notice: New commit pushed; waiting for synchronize event review.")
    elif evidence.get("latest_review_result") == "FAIL":
        print("  -> In Progress: AI reviewer detected defects; awaiting developer fix commit.")
    else:
        print("  -> Idle: No active review loop currently running.")


if __name__ == "__main__":
    main()
