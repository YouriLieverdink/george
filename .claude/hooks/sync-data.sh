#!/bin/bash
set -e
cd "$CLAUDE_PROJECT_DIR"

# Stage only data files
git add data/ 2>/dev/null || true

# Exit if nothing changed
if git diff --cached --quiet; then
  exit 0
fi

# Commit with summary of changed files
CHANGED=$(git diff --cached --name-only | sed 's|data/||' | tr '\n' ', ' | sed 's/,$//')
git commit -m "chore: sync coaching data [$CHANGED]"

# Pull with rebase to cleanly integrate remote changes, then push
git pull --rebase origin main 2>/dev/null || true
git push origin main
