# Workflow: refactoring

## Guardrails

- Refactors must not change user-visible behavior unless paired with an explicit product change.
- Keep PRs focused: structure **or** behavior, not both at large scale.
- Run architecture validation before and after.

## Approach

1. Characterize current boundaries (feature vs shared vs core).
2. Extract shared UI only when reused by 2+ features with a stable API.
3. Move types with their owning feature; promote to `core/models` only when truly cross-cutting.
4. Replace RxJS UI state with signals incrementally, feature by feature.
5. Update barrels (`index.ts`) and fix imports; do not leave deep cross-feature paths.

## Verify

- [ ] Existing tests still pass (update test setup only when DI surface changed)
- [ ] `npm run validate:architecture`
- [ ] Bundle size spot-check if moving lazy boundaries (`npm run build`)
