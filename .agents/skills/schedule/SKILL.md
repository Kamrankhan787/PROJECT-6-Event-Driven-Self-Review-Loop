---
name: schedule
description: Monitoring and recovery watchdog for Project 6. Inspects pull request review status without replacing the event-driven heartbeat.
---

# /schedule — Monitoring and Recovery Watchdog

## Purpose
Provides secondary monitoring and recovery status checks for Project 6.

> [!IMPORTANT]
> - **Primary heartbeat:** GitHub Pull Request event (`opened`, `synchronize`, `reopened`).
> - **Secondary watchdog:** Schedule (monitoring and recovery only).
> The scheduled mechanism must never be presented as the event-driven mechanism.

## Checks Performed
1. Pull request existence and status (open/closed).
2. Latest commit SHA vs reviewed commit SHA.
3. Review status (`FAIL`, `PASS`, or pending).
4. GitHub Actions workflow execution status.
5. Detection of stale reviews or failed runs.

## Execution
```bash
python scripts/schedule.py
```
