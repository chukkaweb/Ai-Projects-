# Workflow: performance

## Measure first

- Reproduce with Angular DevTools / Chrome Performance on the slow route.
- Note whether the cost is change detection, network waterfalls, or bundle size.

## Common fixes (in order)

1. Ensure lists use `@for` with a stable `track`.
2. Avoid recomputing heavy work in templates—use `computed()` in stores.
3. Prefer `OnPush`-friendly patterns (standalone + signals already help).
4. Lazy-load features; keep `shared/` lean.
5. Use `switchMap` for typeahead; debounce at the control layer.
6. Cache idempotent GETs in feature services with clear invalidation rules.
7. Check budgets in `angular.json` after large UI additions.

## Verify

- [ ] Before/after interaction timing or Lighthouse note in the PR
- [ ] No functional regressions on the optimized path
- [ ] `npm run build` within budgets
