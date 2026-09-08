---
name: loop
description: Represents and executes the development verification loop for Project 6, requiring observable evidence before declaring completion.
---

# /loop — Development Verification Loop

## Purpose
Validates the complete development loop using observable evidence:

```text
INSPECT
 ↓
IMPLEMENT
 ↓
TEST
 ↓
CHECK WORKFLOW
 ↓
CHECK PR
 ↓
CHECK REVIEW
 ↓
IDENTIFY FAILURE
 ↓
FIX
 ↓
VERIFY AGAIN
```

## Completion Criteria
The loop must NOT declare Project 6 complete merely because files exist. It strictly verifies:
- PR opened
- Automatic review received
- Planted bug detected (review FAIL)
- Bug fixed
- Fix pushed
- synchronize event fired
- Second automatic review received
- Second review PASS

## Execution
```bash
python scripts/loop.py
```
