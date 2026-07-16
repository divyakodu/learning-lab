# ui-playwright

Browser-driven UI test suite for resume-app, using Playwright (TypeScript,
Chromium) against the frontend's `data-testid` hooks.

## What this tests

- **Resume list** (`index.html`): the list renders, the known
  `divya-kodukula` link is visible, and clicking it navigates to the
  right detail page
- **Resume detail** (`resume.html`): name/headline/summary render
  correctly for a known slug; an unknown slug shows the "Resume not
  found" message; the back link returns to the list
- **Downloads**: clicking the PDF and DOCX buttons triggers a real
  browser download, and the downloaded file's bytes are checked
  (`%PDF` header / `PK` zip header) -- not just that the click didn't error

## Setup

Requires resume-app running first (`../../resume-app/scripts/start.sh`,
serving at `http://localhost:8080`).

```
./setup.sh
```

Installs npm dependencies into this folder's own `node_modules` (not
global) and downloads the Chromium browser binary Playwright needs.

## Run

```
./run.sh
```

Runs the full suite headless. Extra arguments pass through to
`playwright test`, e.g. `./run.sh --headed` or `./run.sh downloads`.

To point at a different instance:

```
RESUME_APP_URL=https://example.com ./run.sh
```

## Last verified run

```
7 passed (3.7s)
```

## Try breaking this on purpose

Verified, safe, and fully reversible -- make the change, rerun `./run.sh`,
read the failure, then undo it:

- In `../../resume-app/frontend/html-js/js/app.js`, change
  `` `resume-link-${r.slug}` `` to `` `link-${r.slug}` `` in `loadList()`.
  No rebuild needed -- nginx serves that file live from disk, just
  refresh. `resume list renders at least one entry` fails with a 5-second
  timeout: Playwright can't find `getByTestId("resume-link-divya-kodukula")`
  anymore, because the test looks up elements by `data-testid`, not by
  guessing at markup. This is exactly why the frontend carries those
  attributes in the first place.
- In the same file's `loadDetail()`, delete the line
  `document.getElementById("pdf-link").href = ...`. The download tests
  fail -- clicking the button no longer has anywhere to point, so no
  download event ever fires.

Undo each change and rerun `./run.sh` to confirm you're back to 7/7 before
moving on.
