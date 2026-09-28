import { ChangeDetectionStrategy, Component, input } from '@angular/core';
import { ReportDefinition } from '../models/report.model';

@Component({
  selector: 'app-report-card',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <article data-testid="report-card">
      <h3>{{ report().name }}</h3>
      <p>{{ report().description }}</p>
      <span>{{ report().cadence }}</span>
    </article>
  `,
  styles: `
    article {
      padding: 1rem 1.25rem;
      border: 1px solid #d9dee5;
      border-radius: 0.75rem;
      background: #fff;
    }

    h3 {
      margin: 0 0 0.35rem;
    }

    p {
      margin: 0 0 0.75rem;
      color: #5c6570;
    }

    span {
      text-transform: capitalize;
      font-size: 0.8125rem;
      font-weight: 600;
      color: #175cd3;
    }
  `,
})
export class ReportCardComponent {
  readonly report = input.required<ReportDefinition>();
}
