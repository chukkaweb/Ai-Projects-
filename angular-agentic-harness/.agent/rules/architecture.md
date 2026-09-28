# Architecture & folder rules

These rules govern where code lives. Agents must follow them on every change.

## Placement rules

- New business functionality must go inside `features/`.
- Do not put feature-specific logic inside `shared/`.
- `core/` contains application-wide infrastructure only.
- Components should remain presentation-focused.
- API communication belongs in services.
- Business state belongs in the feature state layer.
- Avoid direct API calls from components.

## Layer map

```text
src/app/
├── core/                 # App-wide infrastructure ONLY
│   ├── auth/
│   ├── guards/
│   ├── interceptors/
│   ├── services/         # Shared HTTP façade (e.g. ApiService)
│   └── models/           # Cross-cutting types only
│
├── shared/               # Feature-agnostic reuse ONLY
│   ├── components/
│   ├── directives/
│   ├── pipes/
│   ├── validators/
│   └── utils/
│
└── features/<feature>/   # ALL business functionality
    ├── components/       # Presentation-focused UI
    ├── pages/            # Routed containers (wire store → UI)
    ├── services/         # API / data access
    ├── models/           # Feature API contracts & domain types
    ├── state/            # Business / UI state (signals)
    ├── <feature>.routes.ts
    └── index.ts
```

## Allowed dependency direction

```text
features → shared
features → core
app shell → features (lazy), core, shared

features ✗→ other features
shared   ✗→ features
core     ✗→ features
components ✗→ HttpClient / ApiService (use feature services via store)
```

## Decision guide

| Need | Put it in |
|------|-----------|
| New screen or business capability | `features/<name>/` |
| HTTP call for a feature | `features/<name>/services/` |
| Loading / filtered lists / form draft state | `features/<name>/state/` |
| Dumb UI used by one feature | `features/<name>/components/` |
| Dumb UI used by 2+ features | `shared/components/` |
| Auth, guards, interceptors, API base client | `core/` |

## Forbidden

- Feature logic or models in `shared/`
- Domain logic in `core/` beyond infrastructure
- `HttpClient` or direct API calls inside components
- Duplicating the same model in multiple features (promote to `core/models` only when truly shared)
