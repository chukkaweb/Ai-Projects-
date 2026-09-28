import { ComponentFixture, TestBed } from '@angular/core/testing';
import { MetricCardComponent } from './metric-card.component';

describe('MetricCardComponent', () => {
  let fixture: ComponentFixture<MetricCardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MetricCardComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(MetricCardComponent);
    fixture.componentRef.setInput('metric', {
      id: 'm1',
      label: 'Revenue',
      value: 99,
      trendPercent: -2.5,
    });
    fixture.detectChanges();
  });

  it('renders label, value, and trend', () => {
    const text = (fixture.nativeElement as HTMLElement).textContent ?? '';
    expect(text).toContain('Revenue');
    expect(text).toContain('99');
    expect(text).toContain('-2.5%');
  });
});
