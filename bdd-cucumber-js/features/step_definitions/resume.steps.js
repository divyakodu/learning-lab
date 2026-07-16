const assert = require("assert");
const fs = require("fs");
const os = require("os");
const path = require("path");
const { After, Before, Then, When } = require("@cucumber/cucumber");
const { chromium } = require("playwright");

const BASE_URL = process.env.RESUME_APP_URL || "http://localhost:8080";

Before(async function () {
  this.downloadDir = fs.mkdtempSync(path.join(os.tmpdir(), "bdd-cucumber-downloads-"));
  this.browser = await chromium.launch({ headless: true });
  this.context = await this.browser.newContext({ acceptDownloads: true });
  this.page = await this.context.newPage();
});

After(async function () {
  await this.browser.close();
  fs.rmSync(this.downloadDir, { recursive: true, force: true });
});

When("I open the resume list", async function () {
  await this.page.goto(`${BASE_URL}/index.html`);
});

Then("I should see a link for {string}", async function (slug) {
  const visible = await this.page.getByTestId(`resume-link-${slug}`).isVisible();
  assert.ok(visible);
});

When("I open the resume detail page for {string}", async function (slug) {
  await this.page.goto(`${BASE_URL}/resume.html?slug=${slug}`);
});

Then("I should see the name {string}", async function (name) {
  const text = await this.page.getByTestId("resume-name").textContent();
  assert.strictEqual(text, name);
});

Then("I should see a not-found message", async function () {
  const text = await this.page.getByTestId("resume-name").textContent();
  assert.strictEqual(text, "Resume not found");
});

When("I download the PDF for {string}", async function (slug) {
  await this.page.goto(`${BASE_URL}/resume.html?slug=${slug}`);
  const [download] = await Promise.all([
    this.page.waitForEvent("download"),
    this.page.getByTestId("download-pdf").click(),
  ]);
  this.downloadedPath = await download.path();
});

Then("the downloaded file should be a valid PDF", function () {
  const buf = fs.readFileSync(this.downloadedPath);
  assert.strictEqual(buf.subarray(0, 4).toString(), "%PDF");
});

When("I download the DOCX for {string}", async function (slug) {
  await this.page.goto(`${BASE_URL}/resume.html?slug=${slug}`);
  const [download] = await Promise.all([
    this.page.waitForEvent("download"),
    this.page.getByTestId("download-docx").click(),
  ]);
  this.downloadedPath = await download.path();
});

Then("the downloaded file should be a valid DOCX", function () {
  const buf = fs.readFileSync(this.downloadedPath);
  assert.strictEqual(buf.subarray(0, 2).toString(), "PK");
});
