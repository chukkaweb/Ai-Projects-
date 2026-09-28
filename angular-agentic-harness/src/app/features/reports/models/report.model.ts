export interface ReportDefinition {
  id: string;
  name: string;
  description: string;
  cadence: 'daily' | 'weekly' | 'monthly';
}
