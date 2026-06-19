# Throughline

A research companion for writing. The user dumps a messy idea for a piece they want to write;
the app breaks it into angles, curates a reading list per angle, and quizzes the user on each
article so they absorb the sources before writing. Full concept + data model + API contract
live in `docs/throughline-design-spec.md` — read it before starting work.

## Learning mode — read this first

This is a learning project. The two goals are (1) the user becoming fluent in TypeScript and
(2) understanding how the frontend and backend integrate. So:

- **Explain your choices as you go**, especially anything touching the FE↔BE boundary, the
  typed API client, or TypeScript types. Don't silently generate large amounts of code.
- When you write the agents, **show the JSON parsing and error handling** — don't assume the
  model returns clean output. This is where these apps get flaky and it's worth understanding.
- Prefer small, reviewable steps over big drops. Pause at natural checkpoints so the user can
  read and ask questions.
- If a decision has real tradeoffs, surface them instead of just picking.

## Stack

- **Frontend:** React + TypeScript (strict) + Vite + Tailwind, in `frontend/`
- **Backend:** FastAPI + SQLAlchemy + Pydantic (Python), in `backend/`
- **Agents:** Claude Agent SDK (Decomposer, Curator, Quizmaster — see spec §5)
- **Search/content:** Exa or Tavily API (returns cleaned article text — do NOT build a scraper)
- **DB:** SQLite for now (`*.db`, gitignored)

## Repo structure

```
/
├── CLAUDE.md
├── README.md
├── docs/throughline-design-spec.md
├── backend/      # FastAPI app, SQLAlchemy models, agents
└── frontend/     # Vite + React + TS + Tailwind
```

## The integration contract (most important convention)

The Pydantic models are the **single source of truth** for API types. FastAPI generates an
OpenAPI schema from them; the frontend's TypeScript client is **generated** from that schema
(`openapi-typescript` or `orval`), never hand-written. When a backend model changes,
regenerate the client. A type mismatch should be a compile error, not a runtime surprise.

## Conventions

- TypeScript strict mode on; no `any` without a comment justifying it.
- API base URL on the frontend comes from an env var — never hardcoded.
- Keep agents' prompts and parsing in dedicated modules, not inline in route handlers.
- One quiz per article; questions ladder recall → comprehension → synthesis (see spec §5).

## Commands

> Fill these in as Phase 0 sets them up; keep this section current.

- Backend dev: `cd backend && uvicorn app.main:app --reload`
- Frontend dev: `cd frontend && npm run dev`
- Regenerate API client: `cd frontend && npm run gen:api` (backend must be running)

## Current phase

**Phase 1 — Investigations CRUD, no AI yet.** Data model + create/list/view investigations.
Wire the generated TS client. *Teaches: SQLAlchemy, REST, Pydantic↔TS types end to end.*
