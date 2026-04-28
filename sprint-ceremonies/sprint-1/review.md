# Sprint 1 Review

> Filled at the **end** of Sprint 1 during the Sprint Review ceremony.

## Sprint Overview

| Sprint # | Sprint Goal | Start Date | End Date |
|----------|-------------|------------|----------|
| 1 | Kick off CollabAI project by establishing architecture guidelines, core backend foundation (auth + DB), and initializing the React frontend baseline. | 2026-04-28 | 2026-05-07 |

## Completed Work

| Ticket ID | User Story Title | Story Points | Status | Demo Notes |
|-----------|------------------|--------------|--------|------------|
| PM-01 | GitHub Project Setup | 3 | ✅ Done | GitHub Project board configured; labels, milestones, and team access set up. |
| ARCH-01 | DRF + OOP Guidelines | 5 | ❌ Not Done | Carried over — architecture doc in progress. |
| AUTH-01 | Register API | 5 | ❌ Not Done | Blocked until ARCH-01 is merged. |
| DB-01 | Core Models | 6 | ❌ Not Done | Blocked until ARCH-01 is merged. |
| AUTH-02 | Login + JWT | 4 | ❌ Not Done | Blocked until AUTH-01 is complete. |
| MIDDLEWARE-01 | Logging + Auth Middleware | 5 | ❌ Not Done | Blocked until AUTH-01 + AUTH-02 are complete. |
| FE-01 | React + Context Setup | 5 | ❌ Not Done | In progress — React project initialized. |
| FE-02 | Auth UI | 5 | ❌ Not Done | Blocked until AUTH-01 + AUTH-02 are complete. |
| DB-02 | 20+ Models + Migration | 7 | ❌ Not Done | Blocked until DB-01 is complete. |

## Sprint Metrics

| Metric | Value |
|--------|-------|
| Planned SP | 45 |
| Completed SP | 3 |
| Stories Completed | 1 |
| Stories Not Completed | 8 |

- [ ] Sprint goal reached? _(Partially — project infrastructure is set up; backend/frontend work carries over to Sprint 2.)_

## Stakeholder Feedback

- Product Owner noted that the GitHub board and sprint milestones are correctly configured.
- Dependency chain on `ARCH-01` delayed most backend and frontend stories; team to prioritise `ARCH-01` at Sprint 2 start.

## Incomplete Work

- **ARCH-01** — architecture doc not yet merged; carries over to Sprint 2 as top priority.
- **AUTH-01** — blocked by ARCH-01; carries over to Sprint 2.
- **DB-01** — blocked by ARCH-01; carries over to Sprint 2.
- **AUTH-02** — blocked by AUTH-01; carries over to Sprint 2.
- **MIDDLEWARE-01** — blocked by AUTH-01 + AUTH-02; carries over to Sprint 2.
- **FE-01** — in progress; carries over to Sprint 2.
- **FE-02** — blocked by AUTH-01 + AUTH-02; carries over to Sprint 2.
- **DB-02** — blocked by DB-01; carries over to Sprint 2.
