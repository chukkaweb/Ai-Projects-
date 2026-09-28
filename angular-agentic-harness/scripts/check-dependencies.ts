/**
 * Lightweight dependency health check for CI and agents.
 * Run: npx tsx scripts/check-dependencies.ts
 */
import { execSync } from 'node:child_process';
import * as fs from 'node:fs';
import * as path from 'node:path';

const ROOT = path.resolve(__dirname, '..');
const pkgPath = path.join(ROOT, 'package.json');
const pkg = JSON.parse(fs.readFileSync(pkgPath, 'utf8')) as {
  dependencies?: Record<string, string>;
  devDependencies?: Record<string, string>;
};

const deps = { ...pkg.dependencies, ...pkg.devDependencies };
const required = [
  '@angular/core',
  '@angular/common',
  '@angular/router',
  '@angular/forms',
  'rxjs',
  'typescript',
];

const missing = required.filter((name) => !deps[name]);
if (missing.length) {
  console.error('Missing required packages:', missing.join(', '));
  process.exit(1);
}

console.log(`Package manifest OK (${Object.keys(deps).length} dependencies).`);

function printAudit(vulns: Record<string, number>): void {
  console.log(
    `npm audit: critical=${vulns['critical'] ?? 0}, high=${vulns['high'] ?? 0}, moderate=${vulns['moderate'] ?? 0}, low=${vulns['low'] ?? 0}`,
  );
  if ((vulns['critical'] ?? 0) > 0 || (vulns['high'] ?? 0) > 0) {
    console.warn(
      'Review npm audit findings before production release (transitive Angular toolchain advisories are common).',
    );
  }
}

try {
  const output = execSync('npm audit --json', {
    cwd: ROOT,
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'pipe'],
  });
  const audit = JSON.parse(output) as {
    metadata?: { vulnerabilities?: Record<string, number> };
  };
  printAudit(audit.metadata?.vulnerabilities ?? {});
} catch (error) {
  const err = error as { stdout?: string; message?: string };
  if (err.stdout) {
    try {
      const audit = JSON.parse(err.stdout) as {
        metadata?: { vulnerabilities?: Record<string, number> };
      };
      printAudit(audit.metadata?.vulnerabilities ?? {});
    } catch {
      console.warn('Could not parse npm audit JSON; continuing.');
    }
  } else {
    console.warn('npm audit could not run; continuing.', err.message ?? '');
  }
}

console.log('Dependency check passed.');
