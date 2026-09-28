# Testing guide

## Required coverage (every new feature)

- Unit tests (services, stores, utils)
- Component tests (pages + presentational components)
- Playwright e2e for critical user flows under `e2e/<feature>/`

## Before completing a task

```bash
npm run verify
```

UI-critical changes:

```bash
npx playwright install chromium   # once
npm run e2e
```

Full gate:

```bash
npm run verify:full
```

## Unit & component tests

```bash
npm run test:ci
```

Co-locate `*.spec.ts` with sources under `src/app/`.

## E2E (Playwright)

```bash
npm run e2e
npm run e2e:ui
```

Config: `playwright.config.ts`. Prefer `data-testid` selectors.

## Architecture tests

```bash
npm run validate:architecture
```

Fails on cross-feature imports, `HttpClient` in components, missing feature tests/e2e folders, and broken harness files.

See `.agent/rules/testing.md`.
