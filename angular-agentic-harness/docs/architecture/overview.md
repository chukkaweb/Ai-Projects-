# Architecture overview

This application is an **Angular 18 standalone** SPA organized as an agentic harness: human and AI contributors follow the same feature boundaries, rules, and workflows.

## Goals

- Predictable feature isolation for parallel work
- Lazy-loaded routes for scalable bundles
- Signal-first UI state with RxJS at the network edge
- Machine-readable guidance under `.agent/` and `AGENTS.md`

## High-level diagram

```text
Browser
  └─ App shell (nav + router-outlet)
       ├─ core (auth, HTTP, guards)
       ├─ shared (UI primitives)
       └─ features/*
            ├─ dashboard
            ├─ customers
            └─ reports
```

## Related docs

- [Folder structure](./folder-structure.md)
- [State management](./state-management.md)
- [API patterns](./api-patterns.md)
