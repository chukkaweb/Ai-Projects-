# Workflow: bug fix

## 1. Reproduce

- Capture expected vs actual behavior, route, and sample data.
- Add or identify a failing unit/e2e test before changing production code when feasible.

## 2. Isolate

- Search from the UI inward: page → store → service → API/model.
- Check interceptors/guards if the symptom is auth or HTTP related.
- Avoid drive-by refactors unrelated to the defect.

## 3. Fix

- Prefer the smallest change that restores correct behavior.
- Preserve public component inputs/outputs and route paths unless the bug is the contract itself.
- Handle error states explicitly in stores (message + `isLoading`).

## 4. Verify

- [ ] Failing test now passes
- [ ] Nearby regression checks (related store computeds, route guards)
- [ ] `npm run build`

## 5. Report

Summarize root cause, fix, and residual risk in the PR description.
