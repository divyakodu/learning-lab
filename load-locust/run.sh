#!/usr/bin/env bash
# Runs a headless load test against a running resume-app.
# Override defaults with USERS / SPAWN_RATE / RUN_TIME / RESUME_APP_URL env vars.
set -e

cd "$(dirname "$0")"

if [ ! -d .venv ]; then
  echo "No venv found -- run ./setup.sh first."
  exit 1
fi

USERS="${USERS:-20}"
SPAWN_RATE="${SPAWN_RATE:-5}"
RUN_TIME="${RUN_TIME:-30s}"
URL="${RESUME_APP_URL:-http://localhost:8080}"

.venv/bin/locust -f locustfile.py \
  --headless \
  --users "$USERS" \
  --spawn-rate "$SPAWN_RATE" \
  --run-time "$RUN_TIME" \
  --host "$URL" \
  --html report.html \
  --csv report \
  "$@"

echo ""
echo "Full HTML report: report.html"
