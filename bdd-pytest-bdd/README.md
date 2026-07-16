# bdd-pytest-bdd

BDD-style test suite for resume-app, using `pytest-bdd` (Gherkin feature
files + pytest step definitions, Selenium underneath for the actual
browser actions).

## What this tests

Same UI coverage as the other browser stacks, described in
[`features/resume.feature`](features/resume.feature) instead of raw test
functions:

```gherkin
Feature: Resume list and detail

  Scenario: Browsing the resume list
    When I open the resume list
    Then I should see a link for "divya-kodukula"

  Scenario: Downloading a PDF
    When I download the PDF for "divya-kodukula"
    Then the downloaded file should be a valid PDF
```

Plus the detail page, the not-found case, and the DOCX download -- 5
scenarios total, in `test_resume.py`'s step definitions.

## Why BDD, and why this framework specifically

Gherkin's point is that the `.feature` file is readable by someone who
doesn't write code -- a product owner, a manual tester -- while still
being the literal source of truth pytest executes, not documentation
that drifts from what's actually tested. `pytest-bdd` binds Gherkin
steps to plain Python functions decorated with `@when`/`@then`, using
`scenarios("features/resume.feature")` to auto-generate a pytest test
per scenario, and Selenium (reusing the same driver/download-handling
pattern as `selenium-python`) to actually drive the browser.

## Setup

Requires resume-app running first (`../../resume-app/scripts/start.sh`,
serving at `http://localhost:8080`), Python 3, and a real Chrome install.

```
./setup.sh
```

## Run

```
./run.sh
```

Runs all 5 scenarios via `pytest -v`. To point at a different instance:

```
RESUME_APP_URL=https://example.com ./run.sh
```

## Last verified run

```
5 passed in 3.18s
```

## Try breaking this on purpose

Verified, safe, and reversible -- and this failure mode is specific to
BDD tooling, not something the other stacks can produce:

- In `features/resume.feature`, change the step text
  `Then I should see a link for "divya-kodukula"` to
  `Then I should see a resume link for "divya-kodukula"` (just add
  "resume"), without touching `test_resume.py`. Rerun `./run.sh` --
  `test_browsing_the_resume_list` fails immediately with
  `pytest_bdd.exceptions.StepDefinitionNotFoundError: Step definition is
  not found: Then "I should see a resume link for..."`. The Gherkin text
  and the Python step definition are two separate things kept in sync by
  convention, not by the language -- this is what happens the moment
  they drift.

Undo the change and rerun `./run.sh` to confirm you're back to 5/5.
