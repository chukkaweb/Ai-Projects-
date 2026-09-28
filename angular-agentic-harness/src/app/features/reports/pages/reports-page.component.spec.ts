import { ComponentFixture, TestBed } from '@angular/core/testing';
import { signal } from '@angular/core';
import { ReportsPageComponent } from './reports-page.component';
import { ReportsStore } from '../state/reports.store';

describe('ReportsPageComponent', () => {
  let fixture: ComponentFixture<ReportsPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ReportsPageComponent],
      providers: [
        {
          provide: ReportsStore,
          useValue: {
            isLoading: signal(false).asReadonly(),
            items: signal([
              {
                id: 'r1',
                name: 'Usage summary',
                description: 'Daily usage',
                cadence: 'daily',
              },
            ]).asReadonly(),
          },
        },
      ],
    }).compileComponents();

    fixture = TestBed.createComponent(ReportsPageComponent);
    fixture.detectChanges();
  });

  it('renders report cards', () => {
    const text = (fixture.nativeElement as HTMLElement).textContent ?? '';
    expect(text).toContain('Usage summary');
    expect(text).toContain('daily');
  });
});
