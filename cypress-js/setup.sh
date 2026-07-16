#!/usr/bin/env bash
# Installs this stack's node dependencies (scoped to this folder), plus
# the Cypress browser-automation binary (~550MB, downloaded once and
# cached in ~/Library/Caches/Cypress -- shared across projects).
set -e

cd "$(dirname "$0")"

npm install
npx cypress install
npx cypress verify

echo ""
echo "Done. Run tests with: ./run.sh"
