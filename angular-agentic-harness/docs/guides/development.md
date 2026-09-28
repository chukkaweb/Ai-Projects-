# Development guide

## Prerequisites

- Node 20+ (`.nvmrc`)
- npm 10+

## Setup

```bash
npm install
npx playwright install chromium
npm start
```

App: `http://localhost:4200/`

## Day-to-day

| Task | Command |
|------|---------|
| Serve | `npm start` |
| Verify gate | `npm run verify` |
| Full gate + e2e | `npm run verify:full` |
| Unit tests | `npm run test:ci` |
| E2E | `npm run e2e` |
| Lint | `npm run lint` |
| Format | `npm run format` |
| Architecture check | `npm run validate:architecture` |
| Scaffold feature | `npm run generate:feature -- my-feature` |

## Path aliases

| Alias | Target |
|-------|--------|
| `@core` / `@core/*` | `src/app/core` |
| `@shared` / `@shared/*` | `src/app/shared` |
| `@env/*` | `src/environments` |

## Agent loop

1. Read `AGENTS.md` and the matching `.agent/workflows/*` playbook.
2. Implement inside the correct feature folder.
3. Run `npm run verify` before handing off.
4. Update context docs if contracts changed.
