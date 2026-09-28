import { test, expect } from '@playwright/test';

test.describe('Customers critical flow', () => {
  test('filters customers by search', async ({ page }) => {
    await page.goto('/customers');
    await expect(page.getByTestId('page-title')).toHaveText('Customers');
    await expect(page.getByTestId('customers-table')).toBeVisible();

    await page.getByTestId('customers-search').fill('Northwind');
    await expect(page.getByTestId('customers-table')).toContainText('Northwind Labs');
    await expect(page.getByTestId('customers-table')).not.toContainText('Acme Robotics');
  });
});
