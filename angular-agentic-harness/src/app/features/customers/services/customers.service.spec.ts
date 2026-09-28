import { TestBed } from '@angular/core/testing';
import { firstValueFrom } from 'rxjs';
import { CustomersService } from './customers.service';

describe('CustomersService', () => {
  it('returns seeded customers', async () => {
    TestBed.configureTestingModule({});
    const service = TestBed.inject(CustomersService);
    const customers = await firstValueFrom(service.list());
    expect(customers.length).toBeGreaterThan(0);
    expect(customers[0].email).toContain('@');
  });
});
