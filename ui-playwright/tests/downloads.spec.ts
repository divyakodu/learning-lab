import { test, expect } from "@playwright/test";
import * as fs from "fs";

const KNOWN_SLUG = "divya-kodukula";

test("PDF download button produces a real PDF", async ({ page }) => {
  await page.goto(`/resume.html?slug=${KNOWN_SLUG}`);
  const [download] = await Promise.all([
    page.waitForEvent("download"),
    page.getByTestId("download-pdf").click(),
  ]);
  const path = await download.path();
  const buf = fs.readFileSync(path!);
  expect(buf.subarray(0, 4).toString()).toBe("%PDF");
});

test("DOCX download button produces a real DOCX", async ({ page }) => {
  await page.goto(`/resume.html?slug=${KNOWN_SLUG}`);
  const [download] = await Promise.all([
    page.waitForEvent("download"),
    page.getByTestId("download-docx").click(),
  ]);
  const path = await download.path();
  const buf = fs.readFileSync(path!);
  // DOCX is a zip container -- starts with the "PK" local file header signature.
  expect(buf.subarray(0, 2).toString()).toBe("PK");
});
