# Contributing

This project is an **Angular agentic harness**. Humans and coding agents follow the same rules.

## Before you start

1. Read [`AGENTS.md`](./AGENTS.md)
2. Skim [`.agent/rules/architecture.md`](./.agent/rules/architecture.md)
3. Use a playbook from [`.agent/workflows/`](./.agent/workflows/)

## Local setup

```bash
npm install
npm start
```

Node 20+ required (see `.nvmrc`).

## Making changes

- New business work → `src/app/features/<feature>/`
- Reusable UI only → `src/app/shared/`
- Infrastructure only → `src/app/core/`
- Scaffold: `npm run generate:feature -- my-feature`

## Definition of done

Every new feature must include:

- Unit tests (services / stores)
- Component tests (pages / presentational)
- E2E critical-flow coverage under `e2e/<feature>/`

Then run:

```bash
npm run verify
```

Which executes architecture validation, lint, unit tests, and production build.

## Pull requests

Use [`.github/pull_request_template.md`](./.github/pull_request_template.md). Keep PRs focused on one workflow intent when possible.
