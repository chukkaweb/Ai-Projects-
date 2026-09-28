import { TestBed } from '@angular/core/testing';
import { of } from 'rxjs';
import { CustomersService } from '../services/customers.service';
import { CustomersStore } from './customers.store';

describe('CustomersStore', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        CustomersStore,
        {
          provide: CustomersService,
          useValue: {
            list: () =>
              of([
                {
                  id: '1',
                  name: 'Acme',
                  email: 'a@example.com',
                  status: 'active' as const,
                  createdAt: '2026-01-01T00:00:00.000Z',
                },
                {
                  id: '2',
                  name: 'Beta',
                  email: 'b@example.com',
                  status: 'prospect' as const,
                  createdAt: '2026-02-01T00:00:00.000Z',
                },
              ]),
          },
        },
      ],
    });
  });

  it('filters customers by query', () => {
    const store = TestBed.inject(CustomersStore);
    store.setQuery('beta');
    expect(store.filteredCustomers().map((c) => c.name)).toEqual(['Beta']);
  });
});
