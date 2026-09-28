# Security conventions

## Auth & tokens

- Store tokens only via `AuthService` abstractions—never `localStorage` from random components.
- Attach bearer tokens exclusively through `authInterceptor`.
- Route-guard authenticated areas; do not rely on hiding UI alone.

## XSS & templates

- Prefer Angular template binding; avoid `innerHTML` unless sanitized.
- Never interpolate untrusted HTML with `[innerHTML]` without DomSanitizer review.
- Do not use `bypassSecurityTrust*` without an ADR and code review.

## HTTP

- Call APIs only through `ApiService` / feature services using `environment.apiBaseUrl`.
- Do not commit secrets, API keys, or production credentials. Use environment / CI secrets.
- Validate and type API responses at the boundary; do not trust server shapes blindly.

## Dependencies

- Run `npm run check:dependencies` in CI before merge.
- Avoid adding packages with known critical CVEs; prefer maintained Angular-ecosystem libs.
