# Folder structure

```text
src/app/
│
├── core/                      # Application-wide infrastructure ONLY
│   ├── auth/
│   ├── guards/
│   ├── interceptors/
│   ├── services/              # Shared API façade (no feature domain logic)
│   └── models/                # Cross-cutting types only
│
├── shared/                    # Feature-agnostic reuse ONLY
│   ├── components/
│   ├── directives/
│   ├── pipes/
│   ├── validators/
│   └── utils/
│
├── features/                  # ALL business functionality
│   ├── dashboard/
│   │   ├── components/        # Presentation-focused
│   │   ├── pages/             # Routed containers
│   │   ├── services/          # API communication
│   │   ├── models/            # Feature contracts (no duplicates)
│   │   ├── state/             # Business state (signals)
│   │   ├── dashboard.routes.ts
│   │   └── index.ts
│   ├── customers/
│   │   └── … (same layout)
│   └── reports/
│       └── … (same layout)
│
├── app.component.ts
├── app.config.ts
└── app.routes.ts              # Lazy-loads major features
```

## Placement cheat sheet

| Change | Put it in |
|--------|-----------|
| New business functionality | `features/<x>/` |
| API call | `features/<x>/services/` |
| Business / UI state | `features/<x>/state/` |
| Presentation UI (one feature) | `features/<x>/components/` |
| Presentation UI (2+ features) | `shared/components/` |
| Auth, guards, interceptors | `core/` |
| Shared DTO used app-wide | `core/models/` |

## Rules reminder

See `.agent/rules/architecture.md`:

- New business functionality → `features/`
- No feature-specific logic in `shared/`
- `core/` = infrastructure only
- Components = presentation-focused
- API → services; state → feature `state/`
- No direct API calls from components

## Agent / CI companions

| Path | Role |
|------|------|
| `.agent/rules` | Coding standards for agents |
| `.cursor/rules` | Cursor-native rule mirrors |
| `.agent/workflows` | Step-by-step task playbooks |
| `.agent/context` | Condensed domain/architecture memory |
| `scripts/validate-architecture.ts` | Enforces import boundaries |
| `AGENTS.md` | Entry point for coding agents |
| `e2e/<feature>/` | Critical-flow E2E specs |
