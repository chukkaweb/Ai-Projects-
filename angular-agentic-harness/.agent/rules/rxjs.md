# RxJS conventions

## Required

- Use RxJS for asynchronous streams (HTTP, router events, websockets, user event streams).
- Prefer Signals for local UI state derived from those streams.
- Avoid unnecessary subscriptions.
- Prefer `async` pipe or signal interop (`toSignal`, `toObservable`) where appropriate.

## Boundaries

- Bridge streams → signals with `toSignal` / store subscriptions + `takeUntilDestroyed`.
- API communication belongs in services (Observables); business state belongs in feature stores (signals).

## Operators

- Prefer declarative pipes: `map`, `switchMap`, `catchError`, `tap`, `shareReplay({ bufferSize: 1, refCount: true })`.
- Use `switchMap` for latest-only (search/typeahead); `concatMap` for ordered writes; `exhaustMap` for submit buttons.
- Always handle errors near the subscription or with `catchError` that returns a safe fallback.

## Subscriptions

- Prefer `async` pipe or signal conversion over manual `subscribe` in components.
- If you must subscribe in a service/store, pipe `takeUntilDestroyed(destroyRef)`.
- Do not nest `subscribe` calls — compose with operators.

## Forbidden

- Long-lived subscriptions without teardown.
- Subscribing in presentational components.
- Business branching buried inside `tap` when `map`/`filter` would express intent.
