# Features layer

All **business functionality** lives here as vertical slices.

Each feature must include:

```text
<feature>/
  components/   # presentation-focused
  pages/        # routed containers
  services/     # API communication
  models/       # feature contracts (do not duplicate)
  state/        # business state (signals)
  <feature>.routes.ts
  index.ts
```

Rules:

- Lazy-load via `app.routes.ts`
- No imports from other features
- Components do not call APIs directly
- New features also add unit, component, and e2e coverage
