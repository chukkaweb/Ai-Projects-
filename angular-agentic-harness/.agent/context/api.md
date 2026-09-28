# API context (agent)

## Base URL

Configured via `environment.apiBaseUrl` (`src/environments/*`).

All HTTP calls go through `ApiService` or feature services. Components never call `HttpClient` directly.

## Conventions

| Method | Path pattern | Notes |
|--------|--------------|-------|
| GET | `/dashboard/summary` | Returns `DashboardSummary` |
| GET | `/customers` | Returns `Customer[]` |
| GET | `/reports` | Returns `ReportDefinition[]` |

> Seed services currently return fixtures. When wiring a real API, keep these paths and TypeScript models stable or version them deliberately.

## Auth header

`Authorization: Bearer <token>` injected by `authInterceptor` when `AuthService.getAccessToken()` is non-null.

## Errors

- Map HTTP failures in stores to user-safe `error` signals.
- Do not surface raw server stack traces in the UI.
