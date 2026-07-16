#!/usr/bin/env bash
# Runs the API test suite against a running resume-app instance.
# RESUME_APP_URL defaults to http://localhost:8080.
set -e

cd "$(dirname "$0")"

if [ ! -d .venv ]; then
  echo "No venv found -- run ./setup.sh first."
  exit 1
fi

.venv/bin/pytest -v "$@"
