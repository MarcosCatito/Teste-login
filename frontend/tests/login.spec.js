const { test, expect } = require('@playwright/test');

test.describe('Login System E2E Tests', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('should display login form by default', async ({ page }) => {
    await expect(page.locator('h1')).toContainText('Login');
    await expect(page.locator('input[name="username"]')).toBeVisible();
    await expect(page.locator('input[name="password"]')).toBeVisible();
    await expect(page.locator('button[type="submit"]')).toContainText('Login');
  });

  test('should switch to register form', async ({ page }) => {
    await page.click('text=Register');
    await expect(page.locator('h1')).toContainText('Register');
    await expect(page.locator('button[type="submit"]')).toContainText('Register');
  });

  test('should show validation errors for empty fields', async ({ page }) => {
    await page.click('button[type="submit"]');
    
    // Check for HTML5 validation
    const usernameInput = page.locator('input[name="username"]');
    await expect(usernameInput).toBeRequired();
    
    const passwordInput = page.locator('input[name="password"]');
    await expect(passwordInput).toBeRequired();
  });

  test('should register new user successfully', async ({ page }) => {
    // Switch to register form
    await page.click('text=Register');
    
    // Fill registration form
    await page.fill('input[name="username"]', 'testuser123');
    await page.fill('input[name="password"]', 'testpass123');
    
    // Submit form
    await page.click('button[type="submit"]');
    
    // Wait for success message
    await expect(page.locator('.message.success')).toContainText('Registration successful');
    
    // Check localStorage
    const token = await page.evaluate(() => localStorage.getItem('token'));
    const user = await page.evaluate(() => localStorage.getItem('user'));
    expect(token).toBeTruthy();
    expect(user).toBe('testuser123');
  });

  test('should login existing user successfully', async ({ page }) => {
    // First register a user
    await page.click('text=Register');
    await page.fill('input[name="username"]', 'existinguser');
    await page.fill('input[name="password"]', 'existingpass');
    await page.click('button[type="submit"]');
    
    // Wait for registration and redirect
    await page.waitForTimeout(2000);
    
    // Go back to login
    await page.goto('/');
    
    // Fill login form
    await page.fill('input[name="username"]', 'existinguser');
    await page.fill('input[name="password"]', 'existingpass');
    
    // Submit form
    await page.click('button[type="submit"]');
    
    // Wait for success message
    await expect(page.locator('.message.success')).toContainText('Login successful');
  });

  test('should show error for invalid credentials', async ({ page }) => {
    await page.fill('input[name="username"]', 'wronguser');
    await page.fill('input[name="password"]', 'wrongpass');
    await page.click('button[type="submit"]');
    
    await expect(page.locator('.message.error')).toContainText('Invalid credentials');
  });

  test('should handle network errors gracefully', async ({ page }) => {
    // Mock network failure
    await page.route('**/login', route => route.abort());
    
    await page.fill('input[name="username"]', 'testuser');
    await page.fill('input[name="password"]', 'testpass');
    await page.click('button[type="submit"]');
    
    await expect(page.locator('.message.error')).toContainText('Connection error');
  });

  test('should navigate to success page after registration', async ({ page }) => {
    // Switch to register form
    await page.click('text=Register');
    
    // Fill registration form
    await page.fill('input[name="username"]', 'successuser');
    await page.fill('input[name="password"]', 'successpass');
    
    // Submit form
    await page.click('button[type="submit"]');
    
    // Wait for redirect to success page
    await page.waitForURL('/success');
    
    // Check success page content
    await expect(page.locator('h1')).toContainText('Welcome');
    await expect(page.locator('text=Registration Successful')).toBeVisible();
    await expect(page.locator('text=Welcome, successuser')).toBeVisible();
  });

  test('should logout successfully', async ({ page }) => {
    // Register and login first
    await page.click('text=Register');
    await page.fill('input[name="username"]', 'logoutuser');
    await page.fill('input[name="password"]', 'logoutpass');
    await page.click('button[type="submit"]');
    
    // Wait for redirect to success page
    await page.waitForURL('/success');
    
    // Click logout button
    await page.click('button:has-text("Logout")');
    
    // Check redirect to login page
    await expect(page).toHaveURL('/');
    
    // Check localStorage is cleared
    const token = await page.evaluate(() => localStorage.getItem('token'));
    const user = await page.evaluate(() => localStorage.getItem('user'));
    expect(token).toBeNull();
    expect(user).toBeNull();
  });

  test('should be responsive on mobile devices', async ({ page }) => {
    // Test mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });
    
    await expect(page.locator('.container')).toBeVisible();
    await expect(page.locator('h1')).toBeVisible();
    await expect(page.locator('input[name="username"]')).toBeVisible();
    await expect(page.locator('input[name="password"]')).toBeVisible();
  });

  test('should handle form field focus and blur', async ({ page }) => {
    const usernameInput = page.locator('input[name="username"]');
    const passwordInput = page.locator('input[name="password"]');
    
    // Test focus on username field
    await usernameInput.focus();
    await expect(usernameInput).toBeFocused();
    
    // Test tab navigation
    await page.keyboard.press('Tab');
    await expect(passwordInput).toBeFocused();
    
    // Test blur
    await usernameInput.blur();
    await expect(usernameInput).not.toBeFocused();
  });
});
