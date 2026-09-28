# Angular conventions

## Required

- Use standalone components.
- Use lazy-loaded routes for major features.
- Prefer Signals for local UI state.
- Use RxJS for asynchronous streams.
- Avoid unnecessary subscriptions.
- Prefer `async` pipe or signal interop where appropriate.
- Use `ChangeDetectionStrategy.OnPush` on components.
- Prefer `input()` / `output()` signal APIs for new components.

## Defaults

- Do not create NgModules.
- Prefer **Signals** for local and feature UI state. Use RxJS at the HTTP / event boundary.
- Lazy-load each feature via `loadChildren` from `app.routes.ts`.
- Keep feature code inside `src/app/features/<feature>/`. Do not import across features; share via `shared/` or `core/`.
- Prefix selectors with `app-`. Feature host pages live in `pages/`; presentational pieces in `components/`.

## Component rules

- Components should remain **presentation-focused**.
- Pages may inject feature stores and bind signals in templates.
- Presentational components: `@Input` / `@Output` (or `input()` / `output()`) only; **no direct HTTP**.
- Avoid direct API calls from components — go through feature `services/` and `state/`.
- Prefer `input()` / `output()` signal APIs for new code when the surrounding feature already uses them.
- Co-locate template and styles with the component (`templateUrl` / `styleUrl` or inline for tiny UI).

## Routing

- One `*.routes.ts` and barrel `index.ts` per feature.
- Protect authenticated areas with `authGuard` from `core/guards`.
- Set `title` on routes for accessibility and browser chrome.

## DI

- `providedIn: 'root'` for app-wide services and feature stores unless a narrower scope is required.
- Prefer `inject()` over constructor injection for new services/components.

## Forbidden

- Business logic in templates.
- Cross-feature deep imports (e.g. `features/customers` importing from `features/dashboard`).
- Putting feature-specific UI or logic into `shared/`.
- Subscribing in components when `async` pipe or signals suffice.
