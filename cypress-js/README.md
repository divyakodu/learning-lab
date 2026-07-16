# cypress-js

Browser-driven UI test suite for resume-app, using Cypress — the same
coverage as `ui-playwright` and `selenium-python`, in a third automation
model, for direct comparison.

## What this tests

- **Resume list** (`index.html`): the known `divya-kodukula` link is
  visible; clicking it navigates to the right detail page
- **Resume detail** (`resume.html`): name/headline/summary render for a
  known slug; an unknown slug shows the "Resume not found" message; the
  back link returns to the list
- **Downloads**: clicking the PDF and DOCX buttons produces a real
  completed download, verified by the file's magic bytes (`%PDF` / `PK`)

## How this differs from ui-playwright and selenium-python

- **Downloads worked with zero extra configuration.** Playwright has
  `waitForEvent("download")`; Selenium needed real investigation (Chrome
  `prefs` + a CDP command) because headless Chrome blocks downloads by
  default. Cypress's bundled Electron browser just... allows them, and
  `cy.readFile()` against `Cypress.config("downloadsFolder")` (default
  `cypress/downloads`) reads the completed file directly. Verified: both
  download tests passed on the very first run, no workaround needed.
- **Assertions retry automatically, with a real timeout.** `cy.get(...)`
  and `.should(...)` retry for up to 4 seconds by default before failing
  -- closer to Playwright's auto-waiting than Selenium's manual
  `WebDriverWait`, but the retry window is a global default rather than
  written at each call site.
- **Failures capture a screenshot automatically**, saved under
  `cypress/screenshots/` (gitignored, regenerated per run) — worth
  knowing before you wonder where they came from.

## Setup

Requires resume-app running first (`../../resume-app/scripts/start.sh`,
serving at `http://localhost:8080`).

```
./setup.sh
```

Installs npm dependencies into this folder's own `node_modules`, plus
downloads the Cypress binary (~550MB unpacked, cached in
`~/Library/Caches/Cypress` and shared across any project using the same
version — a one-time cost, not per-project).

## Run

```
./run.sh
```

Runs the full suite headless. Extra arguments pass through, e.g.
`./run.sh --spec "cypress/e2e/downloads.cy.js"`.

To point at a different instance:

```
RESUME_APP_URL=https://example.com ./run.sh
```

## Last verified run

```
7 passing (937ms)
```

## Known accepted risk

`npm audit` flags 4 moderate vulnerabilities in `@cypress/request`
(Cypress's internal HTTP client, used by `cy.request()`), via transitive
`qs`/`uuid` versions. The fix requires jumping to Cypress 15 (flagged by
npm as a breaking change). Accepted as-is: this is a devDependency only,
the vulnerable code path (`cy.request()`) isn't used anywhere in this
suite (only `cy.visit`/`cy.get`/`cy.readFile`), and the vulnerability
requires crafted input we never pass. Re-evaluate if Cypress 15
stabilizes and a same-major patch becomes available.

## Try breaking this on purpose

Verified, safe, and reversible:

- In `resume-app/frontend/html-js/js/app.js`, change
  `` `resume-link-${r.slug}` `` to `` `link-${r.slug}` `` in `loadList()`
  — no rebuild needed, refresh is enough. Rerun `./run.sh` --
  `resume-list.cy.js` fails on both its tests after Cypress's default
  4-second retry window: `AssertionError: Timed out retrying after
  4000ms: Expected to find element: '[data-testid="resume-link-divya-
  kodukula"]', but never found it.` Two screenshots get saved to
  `cypress/screenshots/` automatically.

Undo the change and rerun `./run.sh` to confirm you're back to 7/7.
