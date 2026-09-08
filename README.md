# Project 6 — Event-Driven Self-Review Loop

An autonomous, event-driven GitHub Pull Request self-review system. External pull request lifecycle events (`pull_request.opened`, `pull_request.synchronize`, `pull_request.reopened`) serve as the asynchronous heartbeat driving automated AI code reviews and quality verification loops.

---

## 🏗️ Architecture

```text
                 ┌──────────────────┐
                 │    Developer     │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │ GitHub Pull Req. │
                 └────────┬─────────┘
                          │
                 opened/reopened
                          │
                          ▼
                 ┌──────────────────┐
                 │  GitHub Actions  │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │   AI Reviewer    │
                 └────────┬─────────┘
                          │
                    ┌─────┴─────┐
                    ▼           ▼
                  FAIL         PASS
                    │
                    ▼
               Fix + Push
                    │
                    ▼
              synchronize
                    │
                    ▼
                 AI Review
                    │
                    ▼
                  PASS
```

---

## 💓 The Four Heartbeats Progression

This project represents the fourth evolutionary stage in the **Loop Engineering** curriculum:

| Stage | Paradigm | Driving Mechanism | Description |
| :--- | :--- | :--- | :--- |
| **Project 1** | **In-Session Heartbeat** | Active execution loop | Agent maintains state and verifies progress within an active conversational session. |
| **Project 2** | **Conditional Heartbeat** | State change triggers | Loop advances reactively based on evaluation of predicates and test outputs. |
| **Project 3** | **Scheduled Heartbeat** | Time intervals (Cron / Timer) | Watchdog loop triggers at fixed time cadences independently of user interaction. |
| **Project 6** | **Event-Driven Heartbeat** | External webhook / Git event | Loop iterates **only** when an external lifecycle event occurs (`pull_request.opened`, `pull_request.synchronize`). |

> [!NOTE]
> **Key Insight:** Project 6 demonstrates a loop whose next iteration is caused entirely by an external event rather than a continuously running process or polling timer. When the developer pushes a fix commit, GitHub's `pull_request.synchronize` event wakes up the review runner automatically.

---

## 🚀 The Synchronize Event — The Heartbeat

The defining requirement of Project 6 is that **the developer never manually requests a review**.

```text
PR opened
   ↓
opened event fires
   ↓
AI Reviewer automatically runs
   ↓
Planted off-by-one bug detected
   ↓
Reviewer posts FAIL comment
   ↓
Developer fixes bug in src/calculator.py
   ↓
git commit & git push
   ↓
pull_request.synchronize event fires automatically
   ↓
AI Reviewer runs again on latest commit SHA
   ↓
Reviewer confirms fix -> PASS
```

### Review Commit Tracking & Noise Prevention
Every automated review identifies the exact commit SHA reviewed:
```text
## 🤖 AI Pull Request Review
Reviewed commit: db89df5 (db89df50e6a989e0f724eb1e3e6ebf540b40f9a8)
### Result: FAIL
```
When subsequent commits are pushed, the workflow queries existing pull request comments and updates the existing review in-place rather than spamming duplicate comments.

---

## 🛠️ Antigravity Commands

This repository implements three Antigravity commands available via CLI scripts and IDE skills:

### 1. `/goal`
Validates the current Project 6 objective against verifiable evidence in the repository.

* **CLI Execution:**
  ```bash
  python scripts/goal.py
  ```
* **Output:**
  ```text
  PROJECT 6 GOAL

  Build an event-driven GitHub Pull Request self-review loop.

  Success requires:
  - automatic PR review
  - planted bug detection
  - bug fix
  - synchronize-triggered second review
  - final PASS
  ```
* **Skill Definition:** `.agents/skills/goal/SKILL.md`

---

### 2. `/loop`
Executes and validates the 9-stage development verification loop:
`INSPECT -> IMPLEMENT -> TEST -> CHECK WORKFLOW -> CHECK PR -> CHECK REVIEW -> IDENTIFY FAILURE -> FIX -> VERIFY AGAIN`.

* **CLI Execution:**
  ```bash
  python scripts/loop.py
  ```
* **Observable Evidence Requirement:**
  The loop strictly rejects declaring completion based merely on file existence. It requires:
  1. PR opened
  2. Automatic review received
  3. Planted bug detected (`FAIL`)
  4. Bug fixed and committed
  5. `synchronize` event fired
  6. Second review received on new commit SHA
  7. Final review `PASS`
* **Skill Definition:** `.agents/skills/loop/SKILL.md`

---

### 3. `/schedule`
Provides a monitoring and recovery watchdog.

* **CLI Execution:**
  ```bash
  python scripts/schedule.py
  ```
* **Distinction:**
  ```text
  Primary heartbeat:
  GitHub Pull Request event (opened, synchronize)

  Monitoring/recovery:
  Schedule watchdog
  ```
* **Audits:**
  - Active PR detection
  - Review freshness (HEAD SHA vs. Reviewed SHA)
  - Stale review detection
  - Final PASS status
* **Skill Definition:** `.agents/skills/schedule/SKILL.md`

---

## 🧪 Testing Requirements & The Three States

The repository enforces three distinct verification states:

### State 1 — Correct Implementation
Clean implementation of `sum_range(numbers)` in `src/calculator.py` summing all elements.
```bash
python -m pytest -v
```
Result: **7 passed in 0.29s (PASS)**.

### State 2 — Planted Bug
Planted off-by-one bug in `src/calculator.py`:
```python
def sum_range(numbers: Sequence[Number]) -> Number:
    # Omits the final element using [:-1]
    return sum(numbers[:-1])
```
- `pytest` detects the omission (`assert sum_range([10, 20, 30]) == 60` fails with `30 == 60`).
- AI Reviewer detects the off-by-one boundary defect and issues `AI REVIEW RESULT: FAIL`.

### State 3 — Fixed Implementation
Restores full summation `sum(numbers)`.
- `pytest` passes all tests.
- AI Reviewer on `synchronize` event issues `AI REVIEW RESULT: PASS`.

---

## 🤖 GitHub Actions Workflow

File: `.github/workflows/ai-pr-review.yml`

```yaml
name: AI PR Self-Review Loop

on:
  pull_request:
    types:
      - opened
      - synchronize
      - reopened

permissions:
  contents: read
  pull-requests: write
```

### Steps:
1. Check out repository with full history (`fetch-depth: 0`).
2. Set up Python and install `requirements.txt`.
3. Execute unit tests with `pytest`.
4. Extract PR number, base ref (`main`), and head commit SHA (`HEAD_SHA`).
5. Generate git diff between base ref and head commit.
6. Run `scripts/ai_reviewer.py` with the diff.
7. Post or update the review comment on the PR via GitHub REST API.
8. Upload review output artifact.

---

## 🔄 End-to-End Simulation & Demonstration Harness

To reproduce the entire event-driven lifecycle locally with verifiable commit tracking:

```bash
python scripts/simulate_event_loop.py
```

Outputs recorded evidence to `logs/review_evidence.json`, `logs/review_1_fail.md`, and `logs/review_2_pass.md`.

---

## 🔒 Security & Best Practices

- **Zero Hardcoded Secrets:** No API keys or tokens are stored in source code or committed to git.
- **Environment & Secrets:** Uses GitHub Actions secrets (`${{ secrets.GEMINI_API_KEY }}` / `${{ secrets.GOOGLE_API_KEY }}`) and native ephemeral `${{ secrets.GITHUB_TOKEN }}`.
- **Least Privilege:** Permissions are restricted strictly to `contents: read` and `pull-requests: write`.
- **Failure Recovery:** If the reviewer encounters unexpected API failures or rate limits, it falls back to semantic static boundary analysis to ensure the verification pipeline never stalls.
