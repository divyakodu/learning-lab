# bdd-cucumber-js

BDD-style test suite for resume-app, using Cucumber.js with Playwright
underneath for the actual browser actions -- the JS-ecosystem BDD tool,
for a third comparison alongside `bdd-pytest-bdd` and `bdd-behave`.

## What this tests

Identical Gherkin coverage to the other two BDD stacks, in
[`features/resume.feature`](features/resume.feature) -- same feature
file content, deliberately, across all three, so only the step-wiring
differs.

## How this differs from the Python BDD stacks

- **Cucumber expressions instead of regex/parse strings.** Steps are
  matched with `{string}` placeholders (e.g. `Then('I should see a link
  for {string}', ...)`) rather than `pytest-bdd`'s `parsers.parse(...)`
  or Behave's `{name}` format strings -- same idea, Cucumber's own
  syntax.
- **State lives on `this` inside each step function**, set up in
  `Before`/`After` hooks (`features/step_definitions/resume.steps.js`)
  -- conceptually the same role as Behave's `context` object or
  pytest-bdd's fixtures, just Cucumber.js's own convention.
- **Downloads use Playwright's `waitForEvent("download")`**, the same
  approach as `ui-playwright` -- no CDP/prefs workaround needed, unlike
  the Selenium-based BDD stacks.
- **The "undefined step" failure looks different again.** All three BDD
  tools fail the same class of bug (Gherkin step text with no matching
  step definition) differently: pytest-bdd raises
  `StepDefinitionNotFoundError` and stops; Behave marks it "undefined"
  and prints a step-stub in Behave's own decorator style; Cucumber.js
  also marks it "undefined" but prints a stub using `{string}` expression
  syntax and a `return 'pending'` placeholder. Verified below.

## Setup

Requires resume-app running first (`../../resume-app/scripts/start.sh`,
serving at `http://localhost:8080`) and Node.js.

```
./setup.sh
```

Installs npm dependencies into this folder's own `node_modules` and
downloads the Chromium binary Playwright needs (shared cache with
`ui-playwright`/`bdd-cucumber-js` if already downloaded).

## Run

```
./run.sh
```

Runs all 5 scenarios. To point at a different instance:

```
RESUME_APP_URL=https://example.com ./run.sh
```

## Last verified run

```
5 scenarios (5 passed)
20 steps (20 passed)
```

## Try breaking this on purpose

Verified, safe, and reversible:

- In `features/resume.feature`, change the step text
  `Then I should see a link for "divya-kodukula"` to
  `Then I should see a resume link for "divya-kodukula"`, without
  touching `features/step_definitions/resume.steps.js`. Rerun
  `./run.sh` -- 4 scenarios still pass, "Browsing the resume list"
  reports `1 undefined`, and Cucumber prints:
  ```
  Then('I should see a resume link for {string}', function (string) {
    // Write code here that turns the phrase above into concrete actions
    return 'pending';
  });
  ```

Undo the change and rerun `./run.sh` to confirm you're back to 5/5.
