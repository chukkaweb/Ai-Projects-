import { test, expect } from '@playwright/test';

test.describe('Auth shell smoke', () => {
  test('app shell navigation is available', async ({ page }) => {
    await page.goto('/');
    await expect(page.getByTestId('app-shell')).toBeVisible();
    await expect(page.getByTestId('nav-dashboard')).toBeVisible();
    await expect(page.getByTestId('nav-customers')).toBeVisible();
    await expect(page.getByTestId('nav-reports')).toBeVisible();
  });
});
