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
