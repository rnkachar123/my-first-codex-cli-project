#!/usr/bin/env bash
set -euo pipefail

REMOTE="${1:-origin}"
BRANCH="${2:-main}"

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Not inside a Git repository."
  exit 1
fi

if ! git remote get-url "$REMOTE" >/dev/null 2>&1; then
  echo "Skipped git pull: remote '$REMOTE' is not configured in this environment."
  echo "To configure it later, run: git remote add $REMOTE https://github.com/<your-username>/my-first-codex-cli-project.git"
  exit 0
fi

echo "Fetching $REMOTE/$BRANCH ..."
git fetch "$REMOTE" "$BRANCH"

echo "Rebasing local branch onto $REMOTE/$BRANCH ..."
git pull --rebase "$REMOTE" "$BRANCH"

echo "Done."
