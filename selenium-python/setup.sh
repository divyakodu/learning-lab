#!/usr/bin/env bash
# Creates a local venv and installs this stack's dependencies.
# Needs a real Chrome installed -- Selenium Manager auto-downloads a
# matching chromedriver, but not the browser itself.
set -e

cd "$(dirname "$0")"

python3 -m venv .venv
.venv/bin/pip install --upgrade pip -q
.venv/bin/pip install -r requirements.txt

echo ""
echo "Done. Run tests with: ./run.sh"
