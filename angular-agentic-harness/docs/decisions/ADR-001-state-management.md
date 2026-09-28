# ADR-001: Signal-based feature stores

## Status

Accepted

## Context

The app needs predictable per-feature state without the ceremony of a global store for a mid-size console.

## Decision

Use Angular **Signals** in `features/<feature>/state/*.store.ts` for UI state. Keep **RxJS** for HTTP and true event streams. Bridge with `takeUntilDestroyed`.

## Consequences

- Pros: Simple DI, excellent template ergonomics, lazy-friendly, low boilerplate.
- Cons: No built-in time-travel; cross-feature coordination requires deliberate service design.
- Migration path: Introduce NgRx/SignalStore only with a new ADR if complexity warrants it.
