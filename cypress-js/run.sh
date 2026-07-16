#!/usr/bin/env bash
# Runs the Cypress UI test suite against a running resume-app.
# RESUME_APP_URL defaults to http://localhost:8080.
set -e

cd "$(dirname "$0")"

if [ ! -d node_modules ]; then
  echo "No node_modules found -- run ./setup.sh first."
  exit 1
fi

npx cypress run "$@"
