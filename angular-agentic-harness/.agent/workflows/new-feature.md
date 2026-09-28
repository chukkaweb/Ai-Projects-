# Workflow: new feature

Use this playbook when adding a user-facing capability.

## 1. Clarify

- Restate the user goal, acceptance criteria, and out-of-scope items.
- Identify the owning feature under `src/app/features/` (or confirm a new feature is required).
- Read `.agent/rules/architecture.md` plus `.agent/context/architecture.md`, `domain.md`, and `api.md`.

## 2. Scaffold

```bash
npm run generate:feature -- <feature-name>
```

Expected tree:

```text
features/<name>/
  components/ pages/ services/ models/ state/
  <name>.routes.ts
  index.ts
  + unit/component specs

e2e/<name>/<name>.critical-flow.spec.ts   # Playwright
```

## 3. Implement

1. Models and API/service methods first (API stays in services).
2. Feature store (signals) second — business state lives here.
3. Presentational components third — `OnPush`, signal `input()`, no direct API calls.
4. Page + lazy routes fourth.
5. Register lazy route in `app.routes.ts`.
6. Add nav link in `app.component` only if the feature is top-level IA.
7. Add/adjust unit, component, and Playwright e2e tests (`data-testid` for critical controls).

## 4. Verify (required)

```bash
npm run verify
npm run e2e
```

## 5. Document

- Update `docs/` or `.agent/context/` if domain or API contracts changed.
- Note any decision that warrants an ADR under `docs/decisions/`.
