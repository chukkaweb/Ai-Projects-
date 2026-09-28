import { ChangeDetectionStrategy, Component, input } from '@angular/core';
import { TruncatePipe } from '@shared';
import { Customer } from '../models/customer.model';

@Component({
  selector: 'tr[app-customer-row]',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [TruncatePipe],
  template: `
    <td>{{ customer().name }}</td>
    <td>{{ customer().email | truncate: 28 }}</td>
    <td>
      <span class="status" [attr.data-status]="customer().status">{{ customer().status }}</span>
    </td>
  `,
  styles: `
    :host td {
      padding: 0.75rem 0.5rem;
      border-bottom: 1px solid #e6eaef;
    }

    .status {
      text-transform: capitalize;
      font-size: 0.8125rem;
      font-weight: 600;
    }

    .status[data-status='active'] {
      color: #027a48;
    }

    .status[data-status='inactive'] {
      color: #b42318;
    }

    .status[data-status='prospect'] {
      color: #b54708;
    }
  `,
})
export class CustomerRowComponent {
  readonly customer = input.required<Customer>();
}
