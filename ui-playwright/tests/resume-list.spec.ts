import { test, expect } from "@playwright/test";

const KNOWN_SLUG = "divya-kodukula";

test("resume list renders at least one entry", async ({ page }) => {
  await page.goto("/index.html");
  await expect(page.getByTestId("resume-list")).toBeVisible();
  await expect(page.getByTestId(`resume-link-${KNOWN_SLUG}`)).toBeVisible();
});

test("clicking a resume link navigates to its detail page", async ({ page }) => {
  await page.goto("/index.html");
  await page.getByTestId(`resume-link-${KNOWN_SLUG}`).click();
  await expect(page).toHaveURL(new RegExp(`resume\\.html\\?slug=${KNOWN_SLUG}`));
  await expect(page.getByTestId("resume-name")).toBeVisible();
});
