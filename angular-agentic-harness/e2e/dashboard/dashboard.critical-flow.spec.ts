import { test, expect } from '@playwright/test';

test.describe('Dashboard critical flow', () => {
  test('shows metrics on the dashboard', async ({ page }) => {
    await page.goto('/dashboard');
    await expect(page.getByTestId('page-title')).toHaveText('Dashboard');
    await expect(page.getByTestId('dashboard-metrics')).toBeVisible();
    await expect(page.getByTestId('metric-card').first()).toBeVisible();
  });
});
