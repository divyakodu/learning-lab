# learning-lab

Test suites that exercise [resume-app](https://github.com/divyakodu/resume-app)
across multiple frameworks. Each subfolder is a self-contained test stack
against the same running app — same assertions in spirit, different tooling,
so the frameworks can be compared directly.

**New to one of these frameworks?** [`docs/index.html`](docs/index.html) is
a learning hub with a step-by-step, build-along tutorial for each stack —
you write the tests yourself, from an empty file, ending at the real suite
in this repo. Each stack's own README below is the reference copy (what's
tested, setup, run); the tutorials are how you'd actually learn the tool.

Every stack follows the same shape:

```
<stack>/
├── README.md      # what this stack tests, setup, run
├── setup.sh       # one-time: creates a venv (or installs local deps) for this stack only
├── run.sh         # runs the suite against a running resume-app
└── requirements.txt (or package.json, etc.)
```

## Prerequisite: resume-app running

All stacks test a live instance of resume-app. Start it first:

```
cd ../resume-app
scripts/start.sh
```

This serves the app at `http://localhost:8080`. Each stack defaults to that
URL; override with an environment variable documented in the stack's README
if you're pointing at something else.

## Stacks

| Stack | Tooling | What it covers | Status |
|---|---|---|---|
| [api-pytest](api-pytest/) | pytest + requests | REST API: health, resume list/detail, PDF/DOCX downloads, nginx load balancing | Done |
| [ui-playwright](ui-playwright/) | Playwright (TS) | Browser-driven UI flows using the frontend's `data-testid` hooks, incl. real PDF/DOCX download verification | Done |
| [selenium-python](selenium-python/) | Selenium (Python) | Same UI coverage as ui-playwright, for direct comparison -- explicit waits, manual download handling | Done |
| [load-locust](load-locust/) | Locust | Load/performance: throughput and response-time percentiles under concurrent load, not just pass/fail | Done |

More stacks (Cypress, etc.) may be added the same way — copy the shape
above.
