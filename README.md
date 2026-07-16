# learning-lab

Test suites that exercise [resume-app](https://github.com/divyakodu/resume-app)
across multiple frameworks. Each subfolder is a self-contained test stack
against the same running app — same assertions in spirit, different tooling,
so the frameworks can be compared directly.

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
| ui-playwright | Playwright (TS) | Browser-driven UI flows using the frontend's `data-testid` hooks | Planned |

More stacks (Selenium, Cypress, etc.) may be added the same way — copy the
shape above.
