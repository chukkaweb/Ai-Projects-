# My Angular App — Agentic Harness

Production-shaped **Angular 18** standalone app with an enforceable agent harness: rules, workflows, architecture validation, Playwright e2e, and CI gates.

## Demo features

- **Dashboard** — signal store + metric cards
- **Customers** — searchable customer directory
- **Reports** — report catalog

## Quick start

```bash
npm install
npx playwright install chromium   # once, for e2e
npm start                         # http://localhost:4200
```

Node 20+ (see `.nvmrc`).

## Commands

| Script | Purpose |
|--------|---------|
| `npm start` | Dev server |
| `npm run verify` | Architecture + lint + unit tests + build |
| `npm run verify:full` | `verify` + Playwright e2e |
| `npm run e2e` | Playwright critical flows |
| `npm run generate:feature -- <name>` | Scaffold feature + tests + e2e stub |
| `npm run format` | Prettier write |

## Core rules

- Business functionality → `features/` only
- No feature-specific logic in `shared/`
- `core/` = application-wide infrastructure only
- Components = presentation-focused (`OnPush`); API in services; state in feature `state/`
- Standalone + lazy routes; Signals for UI state; RxJS for async streams
- Strict TypeScript; no `any`; no duplicate models
- Every feature: unit + component + Playwright e2e
- Before complete: `npm run verify`

## Agent loop

1. Read [`AGENTS.md`](./AGENTS.md) and [`.agent/README.md`](./.agent/README.md)
2. Follow `.agent/rules/` (+ `.cursor/rules/`)
3. Use a playbook from `.agent/workflows/`
4. Implement inside the owning feature
5. Run `npm run verify` (and `npm run e2e` when UI-critical)

Human contributors: see [`CONTRIBUTING.md`](./CONTRIBUTING.md).

## Layout

See [`docs/architecture/folder-structure.md`](./docs/architecture/folder-structure.md).

```text
src/app/{core,shared,features/<name>/{components,pages,services,models,state}}
.agent/{rules,workflows,context}
e2e/<feature>/
```

## CI

- `.github/workflows/ci.yml` — full verify gate
- `.github/workflows/test.yml` — unit + e2e
- `.github/workflows/build.yml` — production artifact

## Docs

- [Development](./docs/guides/development.md)
- [Testing](./docs/guides/testing.md)
- [Architecture overview](./docs/architecture/overview.md)
- [ADR-001 State](./docs/decisions/ADR-001-state-management.md)
- [ADR-002 Components](./docs/decisions/ADR-002-component-pattern.md)
