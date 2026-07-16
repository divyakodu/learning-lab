# load-locust

Load/performance test suite for resume-app, using Locust. This is a
different kind of test than `api-pytest` or `ui-playwright`: those ask
"does this work?" once; this asks "does this still work well when many
requests hit it at once, and how does it degrade?"

## What this tests

Simulated users repeatedly hit the same endpoints `api-pytest` checks
functionally, at realistic relative frequency (`locustfile.py`):

- `GET /api/resumes` (most common — browsing the list)
- `GET /api/resumes/{slug}` (viewing a resume)
- `GET /api/resumes/{slug}/pdf` / `/docx` (less frequent, heavier — real
  rendering work per request)
- `GET /api/health` (occasional)

Locust reports, per endpoint: requests/sec, failure rate, and response
time percentiles (p50/p90/p95/p99) — not just pass/fail.

## Setup

Requires resume-app running first (`../../resume-app/scripts/start.sh`,
serving at `http://localhost:8080`).

```
./setup.sh
```

Creates a local `.venv` and installs `requirements.txt` into it.

## Run

```
./run.sh
```

Runs headless for 30s with 20 simulated users (spawn rate 5/s), against
`http://localhost:8080`, and writes `report.html` (full charts) plus
`report_*.csv` (raw stats) — both gitignored, regenerated each run.

Override any of it:

```
USERS=50 SPAWN_RATE=10 RUN_TIME=60s RESUME_APP_URL=http://localhost:8080 ./run.sh
```

Or drop into Locust's web UI instead of headless mode:

```
.venv/bin/locust -f locustfile.py --host http://localhost:8080
# then open http://localhost:8089
```

## Last verified run

20 users, 30s, both backend replicas healthy — 414 requests, **0 failures**:

| Endpoint | req/s | p50 | p90 | p99 |
|---|---|---|---|---|
| `/api/resumes` | 7.0 | 4ms | 6ms | 31ms |
| `/api/resumes/[slug]` | 5.1 | 5ms | 6ms | 31ms |
| `/api/resumes/[slug]/pdf` | 1.4 | 120ms | 140ms | 190ms |
| `/api/resumes/[slug]/docx` | 0.7 | 46ms | 54ms | 54ms |

PDF is consistently the slowest endpoint — expected, since it's the only
one doing real rendering work (`weasyprint`) rather than serving JSON.

## Try breaking this on purpose

This one's especially worth doing, because the failure it reveals
**doesn't show up as a failure** in the usual sense — it's exactly the
kind of problem functional tests can't catch, which is the whole reason
load testing exists as a separate discipline:

```
cd ../../resume-app
docker compose stop backend2
cd ../learning-lab/load-locust
RUN_TIME=20s ./run.sh
```

Verified result: **failure rate stays 0%** (nginx silently retries
requests that hit the dead `backend2` onto `backend1`), but **p90 latency
jumps from ~50ms to ~7.6 seconds, and p99 to ~13-14 seconds**. Every
request still eventually succeeds -- a quick smoke test would show all
green -- but the app is in real trouble, and only the percentile numbers
show it.

Restore it and confirm recovery:

```
cd ../../resume-app
docker compose start backend2
cd ../learning-lab/load-locust
./run.sh
```
