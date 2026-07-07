#!/usr/bin/env bash
# Non-interactive bootstrap for opencode: inject the OpenRouter key from an
# environment variable so we never hit the interactive `opencode auth login`
# flow. Runs before `opencode web` (CMD is `./init.sh && opencode web`).
set -euo pipefail

if [ -z "${OPENROUTER_API_KEY:-}" ]; then
  echo "ERROR: OPENROUTER_API_KEY is not set. Pass it to the container, e.g.:" >&2
  echo "  docker run -e OPENROUTER_API_KEY=sk-or-... ..." >&2
  exit 1
fi

# opencode reads provider credentials from auth.json (same file `opencode auth
# login` writes). Writing it here bypasses the interactive login.
AUTH_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/opencode"
mkdir -p "$AUTH_DIR"

cat > "$AUTH_DIR/auth.json" <<EOF
{
  "openrouter": {
    "type": "api",
    "key": "${OPENROUTER_API_KEY}"
  }
}
EOF
chmod 600 "$AUTH_DIR/auth.json"

echo "opencode: OpenRouter credentials configured from OPENROUTER_API_KEY."
