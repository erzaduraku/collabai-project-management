# Sprint 2 Planning

> Filled at the **beginning** of Sprint 2 during the Sprint Planning ceremony.

## Sprint Goal

| Sprint # | Goal | Start Date | End Date |
|----------|------|------------|----------|
| 2 | Build core API infrastructure (CRUD endpoints, multi-tenancy, caching), set up CI/CD, and expand the frontend with a dashboard, task board, and role management UI. | 2026-05-08 | 2026-05-14 |

## Team Capacity

| Team Member | Available Hours | Notes |
|-------------|-----------------|-------|
| erzaduraku | | Backend APIs + CI/CD + caching |
| edonitagashi | | Frontend (dashboard + task board) |
| LeonaZullufi | | Multi-tenancy + DB isolation |
| engjiosmani | | Extra endpoints + auth integration |
| fatlindaosdautaj | | Frontend (role UI) + E2E tests |

## Selected User Stories

| Ticket ID | User Story Title | Story Points | Assignee |
|-----------|------------------|--------------|----------|
| MT-01 | Multi-Tenancy Data Isolation | 5 | LeonaZullufi |
| API-01 | CRUD APIs | 6 | erzaduraku |
| CI-01 | GitHub Actions CI/CD | 5 | erzaduraku |
| FE-03 | Dashboard | 5 | edonitagashi |
| FE-04 | Task Board | 5 | edonitagashi |
| TEST-01 | Unit Tests | 5 | engjiosmani |
| CACHE-01 | Redis Caching | 5 | erzaduraku |
| FE-05 | Role UI | 3 | fatlindaosdautaj |
| API-02 | Extra Endpoints | 5 | engjiosmani |
| TEST-02 | E2E Tests | 6 | fatlindaosdautaj |

## Sprint Summary

| Metric | Value |
|--------|-------|
| Total Planned SP | 50 |
| Total Stories | 10 |
| Team Velocity (prev) | 3 SP (Sprint 1 actual) |

## Notes

- Dependencies to watch:
  - `MT-01` and `API-01` both depend on `DB-02` (carried over from Sprint 1).
  - `FE-03` and `FE-04` depend on `API-01`.
  - `FE-05` depends on `AUTH-02` (carried over from Sprint 1).
  - `API-02` depends on `API-01`.
  - `TEST-01` depends on `API-01`.
  - `TEST-02` depends on `FE-03`, `FE-04`, `AUTH-02`, and `API-01`.
  - `CI-01` depends on `PM-01` (completed in Sprint 1 ✅).
- All Sprint 1 carry-over stories (`ARCH-01`, `AUTH-01`, `DB-01`, `AUTH-02`, `MIDDLEWARE-01`, `FE-01`, `FE-02`, `DB-02`) must be resolved first to unblock this sprint.
