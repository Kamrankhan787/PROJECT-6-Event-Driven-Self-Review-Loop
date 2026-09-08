---
name: goal
description: Inspects and displays the Project 6 goal, success criteria, current implementation status, and remaining work.
---

# /goal — Project 6 Goal Verification

## Purpose
Displays and validates the objective for **PROJECT 6: Event-Driven Self-Review Loop**.

When invoked, the command executes `python scripts/goal.py` and reports:
1. The project goal and completion criteria:
   - Automatic PR review
   - Planted bug detection
   - Bug fix
   - Synchronize-triggered second review
   - Final PASS
2. Concrete inspection of the repository:
   - Python application status
   - Test suite status
   - GitHub Actions workflow status
   - Event-driven evidence tracking (first FAIL, second PASS)
   - Completed requirements vs remaining work

## Execution
```bash
python scripts/goal.py
```
