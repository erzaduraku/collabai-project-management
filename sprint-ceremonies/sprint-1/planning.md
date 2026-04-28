# Sprint 1 Planning

> Filled at the **beginning** of Sprint 1 during the Sprint Planning ceremony.

## Sprint Goal

| Sprint # | Goal | Start Date | End Date |
|----------|------|------------|----------|
| 1 | Kick off CollabAI project by establishing architecture guidelines, core backend foundation (auth + DB), and initializing the React frontend baseline. | 2026-04-28 | 2026-05-07 |

## Team Capacity

| Team Member | Available Hours | Notes |
|-------------|-----------------|-------|
| erzaduraku | | Backend + coordination |
| edonitagashi | | Frontend + architecture doc |
| LeonaZullufi | | Database models + migrations |
| engjiosmani | | Auth (JWT) |
| fatlindaosdautaj | | No stories assigned this sprint |

## Selected User Stories

| Ticket ID | User Story Title | Story Points | Assignee |
|-----------|------------------|--------------|----------|
| PM-01 | GitHub Project Setup | 3 | erzaduraku |
| ARCH-01 | DRF + OOP Guidelines | 5 | edonitagashi |
| AUTH-01 | Register API | 5 | erzaduraku |
| DB-01 | Core Models | 6 | LeonaZullufi |
| AUTH-02 | Login + JWT | 4 | engjiosmani |
| MIDDLEWARE-01 | Logging + Auth Middleware | 5 | erzaduraku |
| FE-01 | React + Context Setup | 5 | edonitagashi |
| FE-02 | Auth UI | 5 | edonitagashi |
| DB-02 | 20+ Models + Migration | 7 | LeonaZullufi |

## Sprint Summary

| Metric | Value |
|--------|-------|
| Total Planned SP | 45 |
| Total Stories | 9 |
| Team Velocity (prev) | N/A |

## Notes

- Dependencies to watch:
  - `ARCH-01` is a prerequisite for `AUTH-01` and `DB-01`.
  - `AUTH-01` is a prerequisite for `AUTH-02`.
  - `DB-01` is a prerequisite for `DB-02`.
  - `AUTH-01` + `AUTH-02` are prerequisites for `FE-02` and `MIDDLEWARE-01`.
  - `PM-01` is a prerequisite for `ARCH-01` and `FE-01`.
- Sprint dates: earliest Start Date 2026-04-28 (ARCH-01) → latest Due Date 2026-05-07 (DB-02).
