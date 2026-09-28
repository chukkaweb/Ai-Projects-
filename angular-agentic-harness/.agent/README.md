# Agent harness index

This folder is the **machine-readable contract** for coding agents working in this repo.

| Path | Purpose |
|------|---------|
| `rules/` | Non-negotiable coding standards |
| `workflows/` | Step-by-step playbooks by intent |
| `context/` | Condensed architecture / domain / API memory |

## Start here

1. Root entry: [`../AGENTS.md`](../AGENTS.md)
2. Placement rules: [`rules/architecture.md`](./rules/architecture.md)
3. Pick a workflow under `workflows/`
4. Implement, then run `npm run verify`

## Rule catalog

| File | Topic |
|------|-------|
| `rules/architecture.md` | `features` / `shared` / `core` boundaries |
| `rules/angular.md` | Standalone, Signals, lazy routes |
| `rules/rxjs.md` | Streams, subscriptions, interop |
| `rules/typescript.md` | Strict typing, models |
| `rules/testing.md` | Unit / component / e2e + verify commands |
| `rules/security.md` | Auth, XSS, secrets |

Cursor mirrors live in `.cursor/rules/*.mdc`.
