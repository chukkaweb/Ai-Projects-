# AGENTS.md — Angular agentic harness

This repository is a **production-shaped Angular agent harness**: feature-sliced standalone app + enforceable rules + workflows + CI gates so coding agents and humans ship the same way.

## Quick start for agents

1. Read this file fully.
2. Skim [`.agent/README.md`](./.agent/README.md) then load rules from `.agent/rules/` (Cursor mirrors in `.cursor/rules/`):
   - `architecture.md` — folder placement
   - `angular.md` / `rxjs.md` — Angular & streams
   - `typescript.md` — strict typing
   - `testing.md` — required tests + verify commands
   - `security.md`
3. Pick a workflow in `.agent/workflows/` based on the user intent.
4. Skim `.agent/context/` for architecture, domain, and API contracts.
5. Implement only inside the owning feature (or `core` / `shared` when justified).
6. Finish with `npm run verify` (add `npm run e2e` for UI-critical work).

## Architecture rules (non-negotiable)

- New business functionality must go inside `features/`.
- Do not put feature-specific logic inside `shared/`.
- `core/` contains application-wide infrastructure only.
- Components should remain presentation-focused (`OnPush`, signal `input()`).
- API communication belongs in services.
- Business state belongs in the feature state layer.
- Avoid direct API calls from components (`HttpClient` in components fails validation).

## Angular / TypeScript (non-negotiable)

- Use standalone components; lazy-load major features.
- Prefer Signals for local UI state; RxJS for asynchronous streams.
- Avoid unnecessary subscriptions; prefer `async` pipe or signal interop.
- Strict typing; avoid `any`; prefer interfaces/types for API contracts; do not duplicate models.
- Path aliases available: `@core`, `@shared`, `@env/*`.

## Intent → workflow map

| User intent | Workflow |
|-------------|----------|
| Add a screen / capability | `.agent/workflows/new-feature.md` |
| Fix incorrect behavior | `.agent/workflows/bug-fix.md` |
| Restructure without behavior change | `.agent/workflows/refactoring.md` |
| Improve speed / bundle / CD | `.agent/workflows/performance.md` |

## End-to-end agent loop

```text
Understand → Plan → Implement (models→services→state→UI→routes→tests) → Verify → Handoff
```

### Verify (required before complete)

```bash
npm run verify
# optional for UI-critical changes:
npm run e2e
# or everything:
npm run verify:full
```

`verify` = `validate:architecture` + `lint` + `test:ci` + `build`.

## Scaffolding a feature

```bash
npm run generate:feature -- inventory
```

Creates feature folders, unit/component specs, and a Playwright e2e stub. Register a lazy route in `src/app/app.routes.ts` and optionally add nav in `app.component.ts`.

## Where things live

| Concern | Location |
|---------|----------|
| Agent index | `.agent/README.md` |
| Agent rules | `.agent/rules/` |
| Cursor rule mirrors | `.cursor/rules/` |
| Agent playbooks | `.agent/workflows/` |
| Condensed memory | `.agent/context/` |
| Human contributing guide | `CONTRIBUTING.md` |
| Deep docs | `docs/` |
| Architecture enforcement | `scripts/validate-architecture.ts` |
| CI | `.github/workflows/` |
| E2E critical flows | `e2e/<feature>/` (Playwright) |

## Definition of done

- [ ] Code respects architecture placement rules (validator clean)
- [ ] Types are strict; no new `any`; models not duplicated
- [ ] Loading/error paths handled in stores for async work
- [ ] Unit + component tests for new feature code
- [ ] Playwright e2e for critical user flows
- [ ] `npm run verify` succeeds
- [ ] Context/docs updated when domain or API changed

## Safety

Follow `.agent/rules/security.md`. Do not commit secrets. Do not weaken auth guards or XSS protections for convenience.
