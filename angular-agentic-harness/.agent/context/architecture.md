# Architecture context (agent)

## Layers

| Layer | Path | Responsibility |
|-------|------|----------------|
| Core | `src/app/core` | Auth, guards, interceptors, API façade, cross-cutting models only |
| Shared | `src/app/shared` | Feature-agnostic UI primitives, pipes, directives, validators, utils |
| Features | `src/app/features/*` | **All business functionality**: pages, components, services, models, state, routes |
| App shell | `app.component.*`, `app.routes.ts`, `app.config.ts` | Shell chrome, router, providers |

## Placement rules

- New business functionality → `features/`
- No feature-specific logic in `shared/`
- `core/` = application-wide infrastructure only
- Components = presentation-focused
- API communication → services
- Business state → feature `state/`
- No direct API calls from components

## Dependency direction

```text
features → shared → (utils only)
features → core
app shell → features (lazy), core, shared
features ✗→ other features
```

## State

- Feature stores expose **signals** to pages.
- Services own HTTP/Observables and mapping.
- See `docs/architecture/state-management.md` and ADR-001.

## Routing

- Lazy `loadChildren` per feature route table.
- Default redirect: `/` → `/dashboard`.

## Full rules

See `.agent/rules/architecture.md` and `.agent/rules/angular.md`.
