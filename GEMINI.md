# Antigravity Workspace Configuration — Project 6

Welcome to **PROJECT 6: Event-Driven Self-Review Loop**.

## Architecture & Progression
This repository demonstrates an **event-driven self-review loop** where GitHub pull request lifecycle events (`pull_request.opened`, `pull_request.synchronize`, `pull_request.reopened`) trigger automated AI reviews without manual intervention.

The loop engineering progression:
1. **Project 1** → In-Session Heartbeat
2. **Project 2** → Conditional Heartbeat
3. **Project 3** → Scheduled Heartbeat
4. **Project 6** → Event-Driven Heartbeat

## Project Commands

The following slash commands are registered in this repository:

### `/goal`
- **Purpose**: Displays the Project 6 objective, success criteria, and audits repository status.
- **Backing Script**: [scripts/goal.py](file:///d:/loop%20engineering/PROJECT%206%20—%20Event-Driven%20Self-Review%20Loop/scripts/goal.py)
- **Skill**: `.agents/skills/goal/SKILL.md`

### `/loop`
- **Purpose**: Executes the full development and verification loop (`INSPECT -> IMPLEMENT -> TEST -> CHECK WORKFLOW -> CHECK PR -> CHECK REVIEW -> IDENTIFY FAILURE -> FIX -> VERIFY AGAIN`).
- **Backing Script**: [scripts/loop.py](file:///d:/loop%20engineering/PROJECT%206%20—%20Event-Driven%20Self-Review%20Loop/scripts/loop.py)
- **Skill**: `.agents/skills/loop/SKILL.md`

### `/schedule`
- **Purpose**: Watchdog for monitoring and recovery. Inspects pending reviews, commit alignment, and failure detection.
- **Note**: The schedule is secondary monitoring only; the GitHub PR event is the primary heartbeat.
- **Backing Script**: [scripts/schedule.py](file:///d:/loop%20engineering/PROJECT%206%20—%20Event-Driven%20Self-Review%20Loop/scripts/schedule.py)
- **Skill**: `.agents/skills/schedule/SKILL.md`

## Safety Guidelines
- Never commit API keys, `.env` files, or secrets into git.
- Workflows use least-privilege GitHub Actions tokens (`contents: read`, `pull-requests: write`).
