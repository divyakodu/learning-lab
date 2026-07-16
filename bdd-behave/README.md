# bdd-behave

BDD-style test suite for resume-app, using Behave -- the more
traditional, standalone Python BDD tool (closer in spirit to Ruby's
Cucumber than `pytest-bdd`'s pytest-plugin approach), for direct
comparison.

## What this tests

Identical Gherkin coverage to `bdd-pytest-bdd`, in
[`features/resume.feature`](features/resume.feature) -- resume list,
detail page, the not-found case, and both downloads. Same feature file
content, deliberately, so the two frameworks are directly comparable;
only the step-definition wiring differs.

## How this differs from bdd-pytest-bdd

- **Its own runner, not a pytest plugin.** You run `behave`, not
  `pytest`. There's no fixture injection -- shared state (the driver,
  the download directory) lives on a single `context` object, set up in
  `features/environment.py`'s `before_scenario`/`after_scenario` hooks
  instead of pytest fixtures.
- **A different failure mode for the same class of bug.** Both
  frameworks fail the same way when a Gherkin step's wording doesn't
  match its step definition -- but pytest-bdd calls it "not found" and
  stops there, while Behave calls it "undefined" and prints a ready-to-
  paste step-definition stub for you. Verified below.

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

Runs all 5 scenarios. To point at a different instance:

```
RESUME_APP_URL=https://example.com ./run.sh
```

## Last verified run

```
1 feature passed, 0 failed, 0 skipped
5 scenarios passed, 0 failed, 0 skipped
10 steps passed, 0 failed, 0 skipped, 0 undefined
```

## Try breaking this on purpose

Verified, safe, and reversible:

- In `features/resume.feature`, change the step text
  `Then I should see a link for "divya-kodukula"` to
  `Then I should see a resume link for "divya-kodukula"`, without
  touching `features/steps/resume_steps.py`. Rerun `./run.sh` -- 4
  scenarios still pass, but "Browsing the resume list" fails with `1
  undefined` and Behave prints:
  ```
  You can implement step definitions for undefined steps with these snippets:

  @then(u'I should see a resume link for "divya-kodukula"')
  def step_impl(context):
      raise NotImplementedError(u'STEP: Then I should see a resume link for "divya-kodukula"')
  ```

Undo the change and rerun `./run.sh` to confirm you're back to 5/5.
