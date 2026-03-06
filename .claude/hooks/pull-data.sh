#!/usr/bin/env bash

LOCK_FILE="/tmp/claude-pull-${CLAUDE_SESSION_ID}"

# Exit early if already pulled this session
[ -f "$LOCK_FILE" ] && exit 0

# Pull latest data and create lock file
cd "$CLAUDE_PROJECT_DIR" || exit 1
git pull origin main --ff-only 2>/dev/null
touch "$LOCK_FILE"
