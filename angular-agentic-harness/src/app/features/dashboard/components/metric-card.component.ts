import { ChangeDetectionStrategy, Component, input } from '@angular/core';
import { DashboardMetric } from '../models/dashboard.model';

@Component({
  selector: 'app-metric-card',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <article class="metric" data-testid="metric-card">
      <h3>{{ metric().label }}</h3>
      <p class="value" data-testid="metric-value">{{ metric().value }}</p>
      <p class="trend" [class.positive]="metric().trendPercent >= 0">
        {{ metric().trendPercent >= 0 ? '+' : '' }}{{ metric().trendPercent }}%
      </p>
    </article>
  `,
  styles: `
    .metric {
      padding: 1rem 1.25rem;
      border: 1px solid #d9dee5;
      border-radius: 0.75rem;
      background: #fff;
    }

    h3 {
      margin: 0;
      font-size: 0.875rem;
      color: #5c6570;
      font-weight: 500;
    }

    .value {
      margin: 0.5rem 0 0.25rem;
      font-size: 1.75rem;
      font-weight: 700;
    }

    .trend {
      margin: 0;
      font-size: 0.875rem;
      color: #b42318;
    }

    .trend.positive {
      color: #027a48;
    }
  `,
})
export class MetricCardComponent {
  readonly metric = input.required<DashboardMetric>();
}
