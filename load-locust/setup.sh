#!/usr/bin/env bash
# Creates a local venv and installs this stack's dependencies.
set -e

cd "$(dirname "$0")"

python3 -m venv .venv
.venv/bin/pip install --upgrade pip -q
.venv/bin/pip install -r requirements.txt

echo ""
echo "Done. Run a load test with: ./run.sh"
