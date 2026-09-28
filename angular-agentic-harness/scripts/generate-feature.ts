/**
 * Scaffold a feature slice matching the agentic harness layout.
 * Run: npx tsx scripts/generate-feature.ts inventory
 */
import * as fs from 'node:fs';
import * as path from 'node:path';

const name = process.argv[2];

if (!name || !/^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$/.test(name)) {
  console.error('Usage: npm run generate:feature -- <kebab-case-name>');
  process.exit(1);
}

const pascal = name
  .split('-')
  .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
  .join('');

const routesConst = `${name.replace(/-/g, '_').toUpperCase()}_ROUTES`;
const root = path.resolve(__dirname, '..', 'src', 'app', 'features', name);

if (fs.existsSync(root)) {
  console.error(`Feature already exists: ${name}`);
  process.exit(1);
}

for (const dir of ['components', 'pages', 'services', 'models', 'state']) {
  fs.mkdirSync(path.join(root, dir), { recursive: true });
}

fs.writeFileSync(
  path.join(root, 'models', `${name}.model.ts`),
  `export interface ${pascal}Item {
  id: string;
  name: string;
}
`,
);

fs.writeFileSync(
  path.join(root, 'services', `${name}.service.ts`),
  `import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { ${pascal}Item } from '../models/${name}.model';

@Injectable({ providedIn: 'root' })
export class ${pascal}Service {
  list(): Observable<${pascal}Item[]> {
    return of([]);
  }
}
`,
);

fs.writeFileSync(
  path.join(root, 'state', `${name}.store.ts`),
  `import { DestroyRef, Injectable, inject, signal } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { ${pascal}Service } from '../services/${name}.service';
import { ${pascal}Item } from '../models/${name}.model';

@Injectable({ providedIn: 'root' })
export class ${pascal}Store {
  private readonly api = inject(${pascal}Service);
  private readonly destroyRef = inject(DestroyRef);

  private readonly items = signal<${pascal}Item[]>([]);
  private readonly loading = signal(false);

  readonly list = this.items.asReadonly();
  readonly isLoading = this.loading.asReadonly();

  constructor() {
    this.load();
  }

  load(): void {
    this.loading.set(true);
    this.api
      .list()
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: (items) => {
          this.items.set(items);
          this.loading.set(false);
        },
        error: () => this.loading.set(false),
      });
  }
}
`,
);

fs.writeFileSync(
  path.join(root, 'pages', `${name}-page.component.ts`),
  `import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { PageHeaderComponent } from '@shared';
import { ${pascal}Store } from '../state/${name}.store';

@Component({
  selector: 'app-${name}-page',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [PageHeaderComponent],
  template: \`
    <app-page-header title="${pascal}" subtitle="Generated feature scaffold." />
    @if (store.isLoading()) {
      <p data-testid="${name}-loading">Loading…</p>
    } @else {
      <p data-testid="${name}-count">{{ store.list().length }} items</p>
    }
  \`,
})
export class ${pascal}PageComponent {
  readonly store = inject(${pascal}Store);
}
`,
);

fs.writeFileSync(
  path.join(root, `${name}.routes.ts`),
  `import { Routes } from '@angular/router';
import { ${pascal}PageComponent } from './pages/${name}-page.component';

export const ${routesConst}: Routes = [
  {
    path: '',
    component: ${pascal}PageComponent,
    title: '${pascal}',
  },
];
`,
);

fs.writeFileSync(
  path.join(root, 'index.ts'),
  `export * from './models/${name}.model';
export * from './services/${name}.service';
export * from './state/${name}.store';
export * from './pages/${name}-page.component';
export * from './${name}.routes';
`,
);

fs.writeFileSync(
  path.join(root, 'components', '.gitkeep'),
  `// Presentational components for ${name} go here.\n`,
);

fs.writeFileSync(
  path.join(root, 'services', `${name}.service.spec.ts`),
  `import { TestBed } from '@angular/core/testing';
import { firstValueFrom } from 'rxjs';
import { ${pascal}Service } from './${name}.service';

describe('${pascal}Service', () => {
  it('lists items', async () => {
    TestBed.configureTestingModule({});
    const service = TestBed.inject(${pascal}Service);
    const items = await firstValueFrom(service.list());
    expect(Array.isArray(items)).toBe(true);
  });
});
`,
);

fs.writeFileSync(
  path.join(root, 'state', `${name}.store.spec.ts`),
  `import { TestBed } from '@angular/core/testing';
import { of } from 'rxjs';
import { ${pascal}Service } from '../services/${name}.service';
import { ${pascal}Store } from './${name}.store';

describe('${pascal}Store', () => {
  it('loads items into state', () => {
    TestBed.configureTestingModule({
      providers: [
        ${pascal}Store,
        {
          provide: ${pascal}Service,
          useValue: { list: () => of([{ id: '1', name: 'Sample' }]) },
        },
      ],
    });

    const store = TestBed.inject(${pascal}Store);
    expect(store.list().length).toBe(1);
    expect(store.isLoading()).toBe(false);
  });
});
`,
);

fs.writeFileSync(
  path.join(root, 'pages', `${name}-page.component.spec.ts`),
  `import { ComponentFixture, TestBed } from '@angular/core/testing';
import { signal } from '@angular/core';
import { ${pascal}PageComponent } from './${name}-page.component';
import { ${pascal}Store } from '../state/${name}.store';

describe('${pascal}PageComponent', () => {
  let fixture: ComponentFixture<${pascal}PageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [${pascal}PageComponent],
      providers: [
        {
          provide: ${pascal}Store,
          useValue: {
            isLoading: signal(false).asReadonly(),
            list: signal([{ id: '1', name: 'Sample' }]).asReadonly(),
          },
        },
      ],
    }).compileComponents();

    fixture = TestBed.createComponent(${pascal}PageComponent);
    fixture.detectChanges();
  });

  it('renders page content from the store', () => {
    const text = (fixture.nativeElement as HTMLElement).textContent ?? '';
    expect(text).toContain('${pascal}');
  });
});
`,
);

const e2eDir = path.resolve(__dirname, '..', 'e2e', name);
fs.mkdirSync(e2eDir, { recursive: true });
fs.writeFileSync(
  path.join(e2eDir, `${name}.critical-flow.spec.ts`),
  `import { test, expect } from '@playwright/test';

test.describe('${pascal} critical flow', () => {
  test('loads the ${name} page', async ({ page }) => {
    await page.goto('/${name}');
    await expect(page.getByTestId('page-title')).toHaveText('${pascal}');
  });
});
`,
);

console.log(`Created feature at src/app/features/${name}`);
console.log(`Created e2e stub at e2e/${name}/${name}.critical-flow.spec.ts`);
console.log(`Next: lazy-load ${routesConst} from app.routes.ts`);
