# State management

## Decision summary

Feature state uses **Angular Signals** inside `*.store.ts` classes. RxJS remains the transport for HTTP. See [ADR-001](../decisions/ADR-001-state-management.md).

## Pattern

```text
Page → inject(FeatureStore) → signals in template
Store → FeatureService.get() → Observable → tap/subscribe → signal.set
```

## Rules

- Pages read stores; they do not call `HttpClient`.
- Derived values use `computed()`.
- Loading and error are first-class signals.
- Invalidate/caches live in services with explicit methods—no hidden globals.

## When to introduce a library

Only after multiple features need shared transactional state, time-travel, or cross-tab sync. Until then, keep signal stores local to each feature.
