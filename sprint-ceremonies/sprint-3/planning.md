# Sprint 3 Planning

> Filled at the **beginning** of Sprint 3 during the Sprint Planning ceremony.

## Sprint Goal

| Sprint # | Goal | Start Date | End Date |
|----------|------|------------|----------|
| 3 | Deliver AI-powered task suggestions, async email notifications, advanced search/filtering, full API documentation, and final system integration for demo readiness. | 2026-05-15 | 2026-05-20 |

## Team Capacity

| Team Member | Available Hours | Notes |
|-------------|-----------------|-------|
| erzaduraku | | AI integration + search API + final integration |
| edonitagashi | | AI UI frontend |
| LeonaZullufi | | Swagger documentation |
| engjiosmani | | Async email + background jobs |
| fatlindaosdautaj | | README documentation + E2E carry-over |

## Selected User Stories

| Ticket ID | User Story Title | Story Points | Assignee |
|-----------|------------------|--------------|----------|
| API-03 | Search + Filtering | 5 | erzaduraku |
| AI-01 | OpenAI + Celery Integration | 7 | erzaduraku |
| FE-06 | AI UI | 5 | edonitagashi |
| ASYNC-01 | Email + Background Jobs | 6 | engjiosmani |
| DOC-01 | Swagger API Documentation | 4 | LeonaZullufi |
| DOC-02 | README | 5 | fatlindaosdautaj |
| FINAL-01 | Final Integration | 8 | erzaduraku |

## Sprint Summary

| Metric | Value |
|--------|-------|
| Total Planned SP | 40 |
| Total Stories | 7 |
| Team Velocity (prev) | _Update after Sprint 2 closes_ |

## Notes

- Dependencies to watch:
  - `AI-01` is a prerequisite for `FE-06` and `ASYNC-01`.
  - `API-02` (Sprint 2) is a prerequisite for `API-03`, `AI-01`, and `DOC-01`.
  - `TEST-02` (Sprint 2) and `DOC-01` are prerequisites for `DOC-02`.
  - `FINAL-01` depends on `DOC-02`, `ASYNC-01`, `FE-06`, `TEST-01`, and `API-03` all being complete.
- This is the final sprint — `FINAL-01` must be completed for demo readiness.
- All 20 course requirements are verified as part of `FINAL-01`.
