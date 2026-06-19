# Throughline — Design Spec

A research companion for writing. You dump a messy idea for a piece you want to write,
it breaks the idea into angles, curates a reading list per angle, and quizzes you on each
article so you actually absorb the sources before you sit down to write.

Built as a deliberate learning project: the goals are (1) real TypeScript fluency on the
frontend and (2) a concrete understanding of how a frontend and backend integrate across a
typed API boundary. Stack intentionally mirrors a production AI-tooling stack.

---

## 1. Core user loop

1. **Brain dump.** "I want to investigate AI in K–12 education and how educators are
   burning out — there's a sociopolitical and psychological angle I can't quite see yet."
2. **Decompose.** The app turns that into structured *angles* (sub-questions + search
   queries): educator burnout literature, automation anxiety, labor/policy framing,
   student-side effects, etc.
3. **Curate.** For each angle it pulls real articles, dedupes and ranks them, and writes a
   one-line "why read this" for each.
4. **Read + quiz.** You read; it quizzes you. Questions ladder from recall →
   comprehension → synthesis, where synthesis ties the article back to *what you're
   writing*. That last rung is what makes it a writer's tool, not a trivia game.

---

## 2. Tech stack

| Layer | Choice | Why |
|---|---|---|
| Frontend | React + TypeScript + Vite + Tailwind | Where most of your TS reps live; matches LinkedIn stack |
| Backend | FastAPI + SQLAlchemy (Python) | Matches LinkedIn stack; clean ORM practice |
| LLM agents | Claude Agent SDK | The decompose / curate / quiz logic |
| Search/content | Exa **or** Tavily API | Returns cleaned article text — do NOT build a scraper |
| DB | SQLite (v1) → Postgres later | SQLite keeps v1 zero-config |

**Out of scope for v1:** auth / multi-user (build it single-user), spaced repetition,
deployment. All noted as v2 below.

---

## 3. Architecture — and the seam you're here to learn

Two separate processes that talk over HTTP:

```
┌─────────────────────────┐         ┌──────────────────────────────┐
│  Frontend (Vite dev)    │  HTTP   │  Backend (FastAPI / uvicorn) │
│  React + TS + Tailwind  │ ──────► │  REST API + SQLAlchemy + DB  │
│  typed API client       │ ◄────── │  3 agents via Claude SDK     │
└─────────────────────────┘  JSON   └──────────────┬───────────────┘
                                                    │
                                          ┌─────────▼─────────┐
                                          │  Exa / Tavily API │
                                          │  Anthropic API    │
                                          └───────────────────┘
```

**The single most important learning mechanism: a typed contract across the seam.**
FastAPI auto-generates an OpenAPI schema from your Pydantic models. Run a generator
(`openapi-typescript` or `orval`) against it to produce TypeScript types + a client for the
frontend. Now a field you add to a Pydantic model in Python shows up as a typed field in
your React code, and a mismatch is a compile error — not a runtime surprise. This is the
clearest possible window into "how frontend and backend integrate." Wire it up early and
regenerate whenever the backend changes.

---

## 4. Data model (SQLAlchemy)

One-to-many all the way down — clean relational practice.

- **Investigation** — `id`, `title`, `brain_dump` (raw text), `status`, `created_at`
- **Angle** — `id`, `investigation_id` (FK), `title`, `description`, `search_queries` (JSON), `order`
- **Article** — `id`, `angle_id` (FK), `url`, `title`, `author`, `source`, `summary`,
  `why_read`, `content` (text, nullable — paywalled pieces use the paste fallback),
  `reading_status` (`unread` | `reading` | `read`), `saved_at`
- **Quiz** — `id`, `article_id` (FK), `created_at`
- **Question** — `id`, `quiz_id` (FK), `prompt`, `type` (`recall` | `comprehension` | `synthesis`),
  `options` (JSON, for multiple choice), `answer`, `explanation`
- **Attempt** — `id`, `question_id` (FK), `user_answer`, `is_correct`, `attempted_at`
  *(unused in v1 UI but the table is what makes spaced repetition possible later — cheap to add now)*

---

## 5. The three agents (Claude Agent SDK)

Each agent has a tight input → output contract. Prompt each to return strict JSON; parse and
persist.

**Decomposer** — `brain_dump: str` → `Angle[]` (`{title, description, search_queries[]}`).
Turns a vague idea into 3–6 concrete angles with searchable queries.

**Curator** — `search_queries: str[]` → `Article[]`. Runs queries through Exa/Tavily, dedupes
by URL/title, ranks by relevance, and writes a one-line `why_read` per result. Stores cleaned
`content` when the API returns it.

**Quizmaster** — `article.content: str` + `investigation.title: str` → `Question[]`. Generates
laddered questions: recall (what happened), comprehension (author's central claim + evidence),
synthesis (how this connects to the thing you're writing). The investigation title is what lets
the synthesis rung be personal.

---

## 6. API contract (FastAPI)

| Method | Path | Does |
|---|---|---|
| POST | `/investigations` | Create from `{title, brain_dump}`; runs Decomposer; returns investigation + angles |
| GET | `/investigations` | List all |
| GET | `/investigations/{id}` | One investigation w/ angles + articles |
| POST | `/angles/{id}/curate` | Run Curator for this angle; returns articles |
| POST | `/articles/{id}/quiz` | Run Quizmaster; returns quiz + questions |
| PATCH | `/articles/{id}` | Update `reading_status`, or paste `content` for paywalled pieces |
| POST | `/questions/{id}/attempt` | Record `{user_answer}`; returns correctness + explanation |

---

## 7. Phased build plan

Built so the integration seam exists from day one and is never magic.

**Phase 0 — Prove the seam.** Scaffold `backend/` (FastAPI hello-world) and `frontend/`
(Vite + React + TS). One GET endpoint, rendered on the page. Get CORS, the dev loop, and the
typed client generator working. *Teaches: the whole FE↔BE handshake in miniature.*

**Phase 1 — Investigations CRUD, no AI yet.** Data model + create/list/view investigations.
Wire the generated TS client. *Teaches: SQLAlchemy, REST, Pydantic↔TS types end to end.*

**Phase 2 — Decomposer.** Brain dump → angles. First LLM integration. *Teaches: Agent SDK,
structured JSON output, persisting agent results.*

**Phase 3 — Curator.** Search API → reading list per angle; mark read/unread; paste fallback.
*Teaches: third-party API integration, async work, list/detail UI.*

**Phase 4 — Quizmaster.** Generate quizzes, take them, record attempts, show explanations.
*Teaches: nested data, interactive stateful UI, the full loop closing.*

**Phase 5 — v2 ideas (pick later):** spaced repetition (resurface old questions), an
"assemble my outline" synthesis step, auth/multi-user, and observability via OpenTelemetry +
LangSmith on the agent calls — which is literally the kind of work your internship is about.

---

## 8. Open decisions to pin down before/while building

- **Search API:** Exa vs Tavily — both return cleaned content; pick on free-tier limits.
- **Quiz format:** multiple-choice (easier to auto-grade) vs free-response (richer, needs the
  LLM to grade). Could start MC, add free-response synthesis questions later.
- **Repo layout:** single repo with `backend/` + `frontend/` folders (recommended) vs two repos.
- **Where the API base URL lives:** env var on the frontend from the start, so nothing's hardcoded.
