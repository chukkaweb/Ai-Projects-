# Domain context (agent)

## Product

Internal operations console for workspace operators.

## Bounded contexts (features)

| Feature | Purpose | Key entities |
|---------|---------|--------------|
| Dashboard | At-a-glance operational health | `DashboardMetric`, `DashboardSummary` |
| Customers | Account directory and search | `Customer` |
| Reports | Scheduled insight catalog | `ReportDefinition` |

## Shared domain language

- **Workspace**: tenant boundary for metrics and customers.
- **Customer status**: `active` \| `inactive` \| `prospect`.
- **Report cadence**: `daily` \| `weekly` \| `monthly`.

## Non-goals (current harness)

- Full authentication provider integration (AuthService is a stub suitable for interceptors/guards demos).
- Real backend—services currently seed in-memory data.
