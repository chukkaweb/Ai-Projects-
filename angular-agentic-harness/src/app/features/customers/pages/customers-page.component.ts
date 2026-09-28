import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { PageHeaderComponent } from '@shared';
import { CustomerRowComponent } from '../components/customer-row.component';
import { CustomersStore } from '../state/customers.store';

@Component({
  selector: 'app-customers-page',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [FormsModule, PageHeaderComponent, CustomerRowComponent],
  template: `
    <app-page-header
      title="Customers"
      subtitle="Search and review customer accounts."
    />

    <label class="search">
      <span>Search</span>
      <input
        type="search"
        data-testid="customers-search"
        [ngModel]="store.searchQuery()"
        (ngModelChange)="store.setQuery($event)"
        placeholder="Name or email"
      />
    </label>

    @if (store.isLoading()) {
      <p data-testid="customers-loading">Loading customers…</p>
    } @else {
      <table data-testid="customers-table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          @for (customer of store.filteredCustomers(); track customer.id) {
            <tr app-customer-row [customer]="customer"></tr>
          } @empty {
            <tr>
              <td colspan="3" data-testid="customers-empty">No customers match your search.</td>
            </tr>
          }
        </tbody>
      </table>
    }
  `,
  styles: `
    .search {
      display: flex;
      flex-direction: column;
      gap: 0.35rem;
      margin-bottom: 1rem;
      max-width: 20rem;
    }

    input {
      padding: 0.55rem 0.75rem;
      border: 1px solid #c9d1d9;
      border-radius: 0.5rem;
    }

    table {
      width: 100%;
      border-collapse: collapse;
    }

    th {
      text-align: left;
      padding: 0.5rem;
      border-bottom: 2px solid #d9dee5;
      font-size: 0.8125rem;
      color: #5c6570;
    }
  `,
})
export class CustomersPageComponent {
  readonly store = inject(CustomersStore);
}
