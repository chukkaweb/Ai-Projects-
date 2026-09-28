import { test, expect } from '@playwright/test';

test.describe('Reports critical flow', () => {
  test('lists available reports', async ({ page }) => {
    await page.goto('/reports');
    await expect(page.getByTestId('page-title')).toHaveText('Reports');
    await expect(page.getByTestId('reports-grid')).toBeVisible();
    await expect(page.getByTestId('report-card').first()).toBeVisible();
  });
});
