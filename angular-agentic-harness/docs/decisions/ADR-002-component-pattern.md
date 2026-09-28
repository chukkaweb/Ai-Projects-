# ADR-002: Standalone feature components

## Status

Accepted

## Context

Angular NgModules add indirection for routing and testing. The CLI defaults to standalone APIs.

## Decision

All components, directives, and pipes are **standalone**. Features expose `*.routes.ts` arrays lazy-loaded from `app.routes.ts`. Smart/dumb split: pages vs components. See also `.agent/rules/angular.md`.

## Consequences

- Pros: Clear import graphs, easier tree-shaking, simpler TestBed setup.
- Cons: Import arrays on each component must be maintained; barrels help but can hide cycles—validation script watches feature boundaries.
