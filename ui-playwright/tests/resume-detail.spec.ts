import { test, expect } from "@playwright/test";

const KNOWN_SLUG = "divya-kodukula";

test("detail page shows name, headline, and summary", async ({ page }) => {
  await page.goto(`/resume.html?slug=${KNOWN_SLUG}`);
  await expect(page.getByTestId("resume-name")).toHaveText("Divya Kodukula");
  await expect(page.getByTestId("resume-headline")).not.toBeEmpty();
  const summaryItems = page.getByTestId("resume-summary").locator("li");
  await expect(summaryItems).not.toHaveCount(0);
});

test("back link returns to the resume list", async ({ page }) => {
  await page.goto(`/resume.html?slug=${KNOWN_SLUG}`);
  await page.getByTestId("back-link").click();
  await expect(page).toHaveURL(/index\.html$/);
  await expect(page.getByTestId("resume-list")).toBeVisible();
});

test("unknown slug shows a not-found message", async ({ page }) => {
  await page.goto("/resume.html?slug=does-not-exist");
  await expect(page.getByTestId("resume-name")).toHaveText("Resume not found");
});
