# api-pytest

REST API test suite for resume-app, using pytest + requests.

## What this tests

- `GET /api/health` returns `{"status": "ok", "instance": ...}`
- `GET /api/resumes` lists resume summaries, including the known
  `divya-kodukula` slug, with the expected shape
- `GET /api/resumes/{slug}` returns full resume detail; unknown slugs 404
- `GET /api/resumes/{slug}/pdf` and `/docx` return valid, correctly
  content-typed files; unknown slugs 404
- nginx load balancing: repeated `/api/health` calls round-robin across
  both `backend1` and `backend2`, and responses carry an `X-Served-By`
  header

## Setup

Requires resume-app running first (`../../resume-app/scripts/start.sh`,
serving at `http://localhost:8080`).

```
./setup.sh
```

Creates a local `.venv` and installs `requirements.txt` into it. Only
touches this folder -- no global/system Python packages.

## Run

```
./run.sh
```

Runs the full suite with `pytest -v`. Any extra arguments are passed
through to pytest, e.g. `./run.sh -k pdf` or `./run.sh -x`.

If resume-app isn't reachable, the suite exits immediately with a message
telling you to start it, instead of failing test-by-test.

To point at a different instance (e.g. a deployed one):

```
RESUME_APP_URL=https://example.com ./run.sh
```

## Last verified run

```
10 passed in 0.25s
```

## Try breaking this on purpose

The fastest way to understand what a test actually checks is to make it
fail on purpose, read why, then undo the change. These are all verified,
safe, and fully reversible:

- Comment out `pydyf==0.10.0` in
  `../../resume-app/backend/python-fastapi/requirements.txt`, then
  `docker compose build --no-cache backend1 backend2 && docker compose up -d`
  in `resume-app`. `test_pdf_download` fails -- the PDF endpoint 500s. This
  is the real bug documented in `resume-app/docs/architecture.html`'s fix
  log; the pin is the fix.
- Comment out `add_header X-Served-By $upstream_addr always;` in
  `../../resume-app/nginx/nginx.conf`, then
  `docker compose restart nginx`. `test_served_by_header_present` fails --
  the header just isn't there anymore.
- Comment out `server backend2:8000;` in the `upstream backend_api` block
  of the same `nginx.conf`, then `docker compose restart nginx`.
  `test_health_round_robins_across_both_backends` fails -- every request
  now lands on `backend1`, so the set of instances seen is `{"backend1"}`
  instead of both.

Undo each change and rerun `./run.sh` to confirm you're back to 10/10
before moving on.
