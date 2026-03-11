#!/usr/bin/env bash
cd "$CLAUDE_PROJECT_DIR" || exit 1
git pull origin main --ff-only 2>/dev/null || true
