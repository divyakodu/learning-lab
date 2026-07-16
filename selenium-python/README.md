# selenium-python

Browser-driven UI test suite for resume-app, using Selenium WebDriver
(Python, headless Chrome) — the same coverage as `ui-playwright`, in a
different automation model, for direct comparison.

## What this tests

- **Resume list** (`index.html`): the known `divya-kodukula` link is
  visible; clicking it navigates to the right detail page
- **Resume detail** (`resume.html`): name/headline/summary render for a
  known slug; an unknown slug shows the "Resume not found" message; the
  back link returns to the list
- **Downloads**: clicking the PDF and DOCX buttons produces a real
  completed download, verified by the file's magic bytes (`%PDF` / `PK`)
  — not just that the click didn't error

## How this differs from ui-playwright

Same app, same assertions in spirit, genuinely different mechanics:

- **Waiting is explicit, not automatic.** Playwright auto-waits for
  elements; Selenium doesn't -- every test here uses
  `WebDriverWait(...).until(...)` deliberately. Skip it and you get
  flaky `NoSuchElementException`s on anything that isn't instant.
- **Downloads need manual configuration.** Playwright exposes
  `page.waitForEvent("download")` out of the box. Headless Chrome via
  Selenium has no such hook -- this stack configures a download
  directory two ways at once (Chrome `prefs` in `conftest.py`, and the
  `Page.setDownloadBehavior` CDP command in each download test), then
  polls the filesystem for a completed file. Verified: on the Chrome
  version used to build this, *either* alone is actually sufficient,
  but headless Chrome's download behavior has shifted across versions
  before, so both together is deliberate redundancy, not decoration.

## Setup

Requires resume-app running first (`../../resume-app/scripts/start.sh`,
serving at `http://localhost:8080`), and a real Chrome browser installed
(Selenium Manager auto-downloads a matching `chromedriver`, but not
Chrome itself).

```
./setup.sh
```

Creates a local `.venv` and installs `requirements.txt` into it.

## Run

```
./run.sh
```

Runs the full suite with `pytest -v`. To point at a different instance:

```
RESUME_APP_URL=https://example.com ./run.sh
```

## Last verified run

```
7 passed in 4.90s
```

## Try breaking this on purpose

Verified, safe, and reversible:

- In `conftest.py`'s `driver` fixture, delete the whole
  `opts.add_experimental_option("prefs", ...)` block, **and** in
  `tests/test_downloads.py`, delete both
  `driver.execute_cdp_cmd("Page.setDownloadBehavior", ...)` calls.
  Rerun `./run.sh` — both download tests fail with
  `TimeoutError: No completed download appeared in ...` after 10s. The
  click still fires; Chrome just has nowhere it's allowed to save the
  file in headless mode, so nothing ever appears. Removing only *one*
  of the two mechanisms (prefs or CDP) and leaving the other is **not**
  enough to reproduce this — either alone still works, which is exactly
  why the real code keeps both.

Undo the change and rerun `./run.sh` to confirm you're back to 7/7.
