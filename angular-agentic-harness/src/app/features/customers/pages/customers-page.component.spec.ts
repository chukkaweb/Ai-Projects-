import { ComponentFixture, TestBed } from '@angular/core/testing';
import { signal } from '@angular/core';
import { CustomersPageComponent } from './customers-page.component';
import { CustomersStore } from '../state/customers.store';

describe('CustomersPageComponent', () => {
  let fixture: ComponentFixture<CustomersPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CustomersPageComponent],
      providers: [
        {
          provide: CustomersStore,
          useValue: {
            searchQuery: signal('').asReadonly(),
            isLoading: signal(false).asReadonly(),
            filteredCustomers: signal([
              {
                id: '1',
                name: 'Acme Robotics',
                email: 'ops@acme.example',
                status: 'active',
                createdAt: '2026-01-01T00:00:00.000Z',
              },
            ]).asReadonly(),
            setQuery: jasmine.createSpy('setQuery'),
          },
        },
      ],
    }).compileComponents();

    fixture = TestBed.createComponent(CustomersPageComponent);
    fixture.detectChanges();
  });

  it('renders customer rows', () => {
    const text = (fixture.nativeElement as HTMLElement).textContent ?? '';
    expect(text).toContain('Acme Robotics');
    expect(text).toContain('active');
  });
});
