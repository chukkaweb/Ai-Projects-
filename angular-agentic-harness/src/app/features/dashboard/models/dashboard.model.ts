export interface DashboardMetric {
  id: string;
  label: string;
  value: number;
  trendPercent: number;
}

export interface DashboardSummary {
  metrics: DashboardMetric[];
  lastUpdated: string;
}
