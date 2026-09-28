# API patterns

## Client stack

- `provideHttpClient(withInterceptors([authInterceptor]))` in `app.config.ts`
- `ApiService` for generic verbs against `environment.apiBaseUrl`
- Feature services for domain-specific endpoints and DTO mapping

## Checklist for a new endpoint

1. Add/extend model in the owning feature `models/`.
2. Add method on the feature service (prefer typed `Observable<T>`).
3. Consume from the feature store; expose signals to the page.
4. Document the path in `.agent/context/api.md`.
5. Add HttpTestingController coverage for mapping/error paths.

## Error handling

- Catch at the store boundary; set a user-safe message.
- Log technical detail via a future logging service—do not `console.log` secrets.
