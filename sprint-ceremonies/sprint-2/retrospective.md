# Sprint 2 Retrospective

> Filled at the **end** of Sprint 2, after the Sprint Review ceremony.

## Sprint #: 2

---

## What Worked Well

- CI/CD pipeline (GitHub Actions) gives the team fast feedback on every push.
- Multi-tenancy data isolation was well-designed and did not require rework.
- Daily stand-ups introduced in Sprint 2 helped surface blockers within 24 hours.

## What Needs Improvement

- Carry-over volume from Sprint 1 inflated the Sprint 2 scope unexpectedly.
- End-to-end test setup (`TEST-02`) was complex and should have been split into smaller tasks.
- Frontend and backend work occasionally merged without coordination, causing integration issues.

## Action Items

| Action Item | Owner | Due Date |
|-------------|-------|----------|
| Break any story > 5 SP into sub-tasks during Sprint 3 planning | erzaduraku (Scrum Master) | Sprint 3 planning |
| Agree on a frontend-backend integration checkpoint mid-sprint | edonitagashi + erzaduraku | Sprint 3 — Day 3 |
| Add E2E test scaffolding as a prerequisite before Sprint 3 kicks off | fatlindaosdautaj | Sprint 3 — Day 1 |
| Review carry-over stories before adding new ones to the Sprint 3 backlog | erzaduraku | Sprint 3 planning |

## Retrospective Summary Table

| Worked Well | Needs Improvement | Next Steps |
|-------------|-------------------|------------|
| CI/CD pipeline up and running | Carry-over from Sprint 1 bloated scope | Prioritise carry-over before new work |
| Multi-tenancy isolation implemented cleanly | TEST-02 too large as a single story | Split large stories (> 5 SP) into sub-tasks |
| Daily stand-ups caught blockers quickly | Frontend/backend integration not coordinated | Mid-sprint integration checkpoint |

## Team Mood

> Rate 1–5 (5 = great)

| Team Member | Rating | Comment |
|-------------|--------|---------|
| erzaduraku | 4 | Good progress on APIs; CI/CD is a big quality win. |
| edonitagashi | 3 | Dashboard and task board are solid; integration friction needs addressing. |
| LeonaZullufi | 4 | Multi-tenancy work was complex but rewarding. |
| engjiosmani | 3 | Unit tests reveal some edge cases; need more time for coverage. |
| fatlindaosdautaj | 4 | Role UI shipped cleanly; keen to tackle E2E properly in Sprint 3. |
