# Deployment guide

## Build

```bash
npm run build
```

Output: `dist/my-angular-app/`

Production builds replace `environment.ts` with `environment.production.ts` via `angular.json` file replacements.

## CI

GitHub Actions:

- `ci.yml` — install, lint, architecture validate, test, build
- `test.yml` — unit tests (and e2e when enabled)
- `build.yml` — production artifact upload

## Hosting notes

- Serve `index.html` as the SPA fallback for client routes (`/dashboard`, `/customers`, `/reports`).
- Configure `apiBaseUrl` / reverse proxy so `/api` reaches the backend.
- Never bake secrets into the client bundle; inject runtime config if needed later.
