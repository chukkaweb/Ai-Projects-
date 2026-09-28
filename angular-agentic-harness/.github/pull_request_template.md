## Summary

<!-- What changed and why (1–3 bullets). -->

-

## Workflow followed

<!-- new-feature | bug-fix | refactoring | performance -->

-

## Architecture checklist

- [ ] New business functionality lives in `features/`
- [ ] No feature-specific logic in `shared/`
- [ ] `core/` changes are infrastructure-only
- [ ] Components remain presentation-focused (no direct API calls)
- [ ] API in services; business state in feature `state/`
- [ ] No cross-feature imports
- [ ] Signals for UI state; RxJS at async boundaries
- [ ] Lazy route registered if new feature/page
- [ ] No duplicated models / no new `any`
- [ ] `.agent/context` or `docs/` updated if contracts changed

## Testing checklist

- [ ] Unit tests
- [ ] Component tests
- [ ] E2E for critical user flows (when applicable)

## Verify (required)

- [ ] `npm run verify`
- [ ] `npm run e2e` (UI-critical changes)
- [ ] Manual path:

## Screenshots / notes

<!-- Optional -->
