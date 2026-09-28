# Core layer

Application-wide **infrastructure only**.

Allowed here:

- Auth session handling
- Route guards
- HTTP interceptors
- Generic API client (`ApiService`)
- Cross-cutting models (e.g. `User`)

Not allowed:

- Feature screens
- Feature-specific business rules
- Feature-only models that are not shared
