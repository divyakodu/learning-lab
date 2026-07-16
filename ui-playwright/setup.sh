#!/usr/bin/env bash
# Installs this stack's node dependencies (scoped to this folder) and the
# Playwright browser binary it needs.
set -e

cd "$(dirname "$0")"

npm install
npx playwright install chromium

echo ""
echo "Done. Run tests with: ./run.sh"
