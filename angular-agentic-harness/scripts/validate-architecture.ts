/**
 * Architecture boundary validator for the Angular agentic harness.
 * Run: npm run validate:architecture
 */
import * as fs from 'node:fs';
import * as path from 'node:path';

const ROOT = path.resolve(__dirname, '..');
const APP = path.join(ROOT, 'src', 'app');

const REQUIRED_PATHS = [
  '.agent/README.md',
  '.agent/rules/architecture.md',
  '.agent/rules/angular.md',
  '.agent/rules/typescript.md',
  '.agent/rules/rxjs.md',
  '.agent/rules/testing.md',
  '.agent/rules/security.md',
  '.cursor/rules/architecture.mdc',
  '.cursor/rules/angular.mdc',
  '.cursor/rules/typescript.mdc',
  '.cursor/rules/testing.mdc',
  '.cursor/rules/rxjs.mdc',
  '.cursor/rules/security.mdc',
  '.agent/workflows/new-feature.md',
  '.agent/workflows/bug-fix.md',
  '.agent/workflows/refactoring.md',
  '.agent/workflows/performance.md',
  '.agent/context/architecture.md',
  '.agent/context/domain.md',
  '.agent/context/api.md',
  'AGENTS.md',
  'CONTRIBUTING.md',
  'src/app/core',
  'src/app/shared',
  'src/app/features',
  'src/app/core/README.md',
  'src/app/shared/README.md',
  'src/app/features/README.md',
];

const errors: string[] = [];
const warnings: string[] = [];

function walk(dir: string, acc: string[] = [], predicate: (name: string) => boolean = () => true): string[] {
  if (!fs.existsSync(dir)) {
    return acc;
  }
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.name === 'README.md') {
      continue;
    }
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      walk(full, acc, predicate);
    } else if (predicate(entry.name)) {
      acc.push(full);
    }
  }
  return acc;
}

function read(file: string): string {
  return fs.readFileSync(file, 'utf8');
}

function featureNameFromPath(file: string): string | null {
  const rel = path.relative(path.join(APP, 'features'), file);
  if (rel.startsWith('..')) {
    return null;
  }
  return rel.split(path.sep)[0] ?? null;
}

for (const rel of REQUIRED_PATHS) {
  if (!fs.existsSync(path.join(ROOT, rel))) {
    errors.push(`Missing required path: ${rel}`);
  }
}

const featureRoot = path.join(APP, 'features');
const features = fs.existsSync(featureRoot)
  ? fs
      .readdirSync(featureRoot, { withFileTypes: true })
      .filter((d) => d.isDirectory())
      .map((d) => d.name)
  : [];

for (const feature of features) {
  const required = ['components', 'pages', 'services', 'models', 'state', `${feature}.routes.ts`, 'index.ts'];
  for (const piece of required) {
    if (!fs.existsSync(path.join(featureRoot, feature, piece))) {
      errors.push(`Feature "${feature}" missing ${piece}`);
    }
  }

  const serviceSpecs = walk(path.join(featureRoot, feature, 'services'), [], (n) => n.endsWith('.service.spec.ts'));
  const storeSpecs = walk(path.join(featureRoot, feature, 'state'), [], (n) => n.endsWith('.store.spec.ts'));
  const pageSpecs = walk(path.join(featureRoot, feature, 'pages'), [], (n) => n.endsWith('.spec.ts'));
  if (!serviceSpecs.length) {
    errors.push(`Feature "${feature}" missing service unit test (*.service.spec.ts)`);
  }
  if (!storeSpecs.length) {
    errors.push(`Feature "${feature}" missing store unit test (*.store.spec.ts)`);
  }
  if (!pageSpecs.length) {
    errors.push(`Feature "${feature}" missing page component test (*.spec.ts in pages/)`);
  }

  const e2eDir = path.join(ROOT, 'e2e', feature);
  if (!fs.existsSync(e2eDir)) {
    errors.push(`Feature "${feature}" missing e2e folder: e2e/${feature}/`);
  } else {
    const e2eSpecs = fs.readdirSync(e2eDir).filter((n) => n.endsWith('.spec.ts') || n.endsWith('.spec.js'));
    if (!e2eSpecs.length) {
      errors.push(`Feature "${feature}" missing e2e critical-flow spec under e2e/${feature}/`);
    }
  }
}

const importRe = /from\s+['"]([^'"]+)['"]/g;
const httpClientRe = /\bHttpClient\b/;
const injectHttpRe = /inject\(\s*HttpClient\s*\)/;

const componentFiles = [
  ...walk(path.join(APP, 'features'), [], (n) => n.endsWith('.component.ts')),
  ...walk(path.join(APP, 'shared'), [], (n) => n.endsWith('.component.ts')),
];

for (const file of componentFiles) {
  const rel = path.relative(ROOT, file);
  const source = read(file);
  if (httpClientRe.test(source) || injectHttpRe.test(source)) {
    errors.push(`Component must not use HttpClient directly: ${rel}`);
  }
  if (!source.includes('ChangeDetectionStrategy.OnPush') && !rel.includes('app.component.ts')) {
    warnings.push(`Prefer OnPush change detection: ${rel}`);
  }
}

for (const file of walk(featureRoot, [], (n) => n.endsWith('.ts') && !n.endsWith('.spec.ts'))) {
  const rel = path.relative(ROOT, file);
  const feature = featureNameFromPath(file);
  if (!feature) {
    continue;
  }
  const source = read(file);
  let match: RegExpExecArray | null;
  importRe.lastIndex = 0;
  while ((match = importRe.exec(source))) {
    const spec = match[1];
    if (spec.includes('/features/') || spec.includes('../features/')) {
      const other = spec.match(/features\/([^/]+)/)?.[1];
      if (other && other !== feature) {
        errors.push(`Cross-feature import in ${rel}: ${spec}`);
      }
    }
    if (spec.startsWith('.')) {
      const resolved = path.normalize(path.join(path.dirname(file), spec));
      const marker = `${path.sep}features${path.sep}`;
      if (resolved.includes(marker)) {
        const other = resolved.split(marker)[1]?.split(path.sep)[0];
        if (other && other !== feature) {
          errors.push(`Cross-feature import in ${rel}: ${spec}`);
        }
      }
    }
  }
}

for (const file of walk(path.join(APP, 'shared'), [], (n) => n.endsWith('.ts') && !n.endsWith('.spec.ts'))) {
  const rel = path.relative(ROOT, file);
  const source = read(file);
  if (source.includes('/features/') || /from\s+['"][^'"]*features\//.test(source)) {
    errors.push(`shared/ must not import features: ${rel}`);
  }
  if (httpClientRe.test(source) || injectHttpRe.test(source)) {
    errors.push(`shared/ must not use HttpClient: ${rel}`);
  }
}

for (const file of walk(path.join(APP, 'core'), [], (n) => n.endsWith('.ts') && !n.endsWith('.spec.ts'))) {
  const rel = path.relative(ROOT, file);
  const source = read(file);
  if (/from\s+['"][^'"]*features\//.test(source) || source.includes('../features/')) {
    errors.push(`core/ must not import features: ${rel}`);
  }
}

if (warnings.length) {
  console.warn('Architecture warnings:\n');
  for (const warn of warnings) {
    console.warn(`  ⚠ ${warn}`);
  }
  console.warn('');
}

if (errors.length) {
  console.error('Architecture validation failed:\n');
  for (const err of errors) {
    console.error(`  • ${err}`);
  }
  process.exit(1);
}

console.log(`Architecture OK (${features.length} features, ${componentFiles.length} components checked).`);
