import { ChangeDetectionStrategy, Component, input } from '@angular/core';

@Component({
  selector: 'app-page-header',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <header class="page-header" data-testid="page-header">
      <h1 data-testid="page-title">{{ title() }}</h1>
      @if (subtitle(); as text) {
        <p data-testid="page-subtitle">{{ text }}</p>
      }
    </header>
  `,
  styles: `
    .page-header {
      margin-bottom: 1.5rem;
    }

    h1 {
      margin: 0 0 0.25rem;
      font-size: 1.75rem;
      font-weight: 600;
    }

    p {
      margin: 0;
      color: #5c6570;
    }
  `,
})
export class PageHeaderComponent {
  readonly title = input.required<string>();
  readonly subtitle = input<string>();
}
