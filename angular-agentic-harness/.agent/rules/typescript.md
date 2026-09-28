# TypeScript conventions

## Required

- Enable strict typing (project `tsconfig` already has `"strict": true` — do not weaken it).
- Avoid `any`.
- Prefer interfaces/types for API contracts.
- Do not duplicate models.

## Language level

- Prefer `unknown` over `any`. Narrow with type guards in `shared/utils`.
- Respect `noImplicitOverride`, unused-locals, and Angular strict template checks.

## Types & models

- Domain / API contracts live in `features/<feature>/models/` (or `core/models` only when cross-cutting).
- Prefer `interface` or `type` for request/response shapes — one canonical definition.
- Do not copy-paste the same model into another feature; import the owning model or promote to `core/models`.
- Export public types from the feature `index.ts` only when other layers need them.
- Use `readonly` on DTO fields that must not be mutated by consumers.
- Discriminated unions over boolean flag soup (`status: 'active' | 'inactive'`).

## APIs

- Async APIs return `Observable<T>` from services; stores expose signals to the UI.
- Never leak `HttpClient` into components — wrap with feature services or `ApiService`.

## Style

- Named exports; avoid default exports except where Angular CLI scaffolds require them.
- File names: `kebab-case.suffix.ts` (`customer.model.ts`, `auth.guard.ts`).
- One primary export per file when practical.
