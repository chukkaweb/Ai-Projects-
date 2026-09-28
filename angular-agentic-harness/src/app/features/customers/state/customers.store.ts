import { DestroyRef, Injectable, computed, inject, signal } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { CustomersService } from '../services/customers.service';
import { Customer } from '../models/customer.model';

@Injectable({ providedIn: 'root' })
export class CustomersStore {
  private readonly customersService = inject(CustomersService);
  private readonly destroyRef = inject(DestroyRef);

  private readonly customers = signal<Customer[]>([]);
  private readonly loading = signal(false);
  private readonly query = signal('');

  readonly isLoading = this.loading.asReadonly();
  readonly searchQuery = this.query.asReadonly();
  readonly filteredCustomers = computed(() => {
    const q = this.query().trim().toLowerCase();
    const list = this.customers();
    if (!q) {
      return list;
    }
    return list.filter(
      (c) => c.name.toLowerCase().includes(q) || c.email.toLowerCase().includes(q),
    );
  });

  constructor() {
    this.load();
  }

  load(): void {
    this.loading.set(true);
    this.customersService
      .list()
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: (customers) => {
          this.customers.set(customers);
          this.loading.set(false);
        },
        error: () => this.loading.set(false),
      });
  }

  setQuery(value: string): void {
    this.query.set(value);
  }
}
