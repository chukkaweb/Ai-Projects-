# Testing conventions

## Required for every new feature

- Unit tests (services, stores, utilities)
- Component tests (pages and presentational components)
- E2E test for critical user flows (`e2e/<feature>/`)

## Before completing a task, run

```bash
npm run verify
```

Which runs architecture validation, lint, unit/component tests, and production build.

For critical UI flows also run:

```bash
npm run e2e
```

Or the full gate:

```bash
npm run verify:full
```
## Unit tests

- Use Jasmine + Karma (`*.spec.ts` next to source).
- Cover services and stores: loading, success, error, and derived computed signals.
- Prefer testing public behavior over private methods.

## Component tests

- TestBed: import standalone components under test; stub stores/services.
- Assert DOM contracts, inputs/outputs, and empty/loading/error UI states.

## E2E

- Place specs under `e2e/<feature>/` (and `e2e/auth/` for auth journeys).
- Cover the critical happy path for each major feature.
- Use stable `data-testid` attributes for interactive controls.
- Keep e2e independent of implementation details (no brittle class-name assertions).

## What to mock

- Mock HTTP with `HttpClientTestingModule` / `HttpTestingController` for API services.
- Do not mock what you own inside the same unit unless it creates heavy I/O.

## Commands

| Command | Purpose |
|---------|---------|
| `npm run lint` | ESLint |
| `npm test` | Unit + component tests |
| `npm run build` | Production build |
| `npm run validate:architecture` | Folder / import boundaries |
| `npm run e2e` | E2E (when Playwright/Cypress is wired) |
