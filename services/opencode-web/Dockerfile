# opencode web: headless OpenCode server + web UI, pinned to a fixed version
# with auto-update disabled. Default model is GLM-5.2 via OpenRouter; the
# OpenRouter key is injected at runtime by init.sh (no interactive login).
#
# Two-stage build: `opencode` ships as a self-contained Bun binary, so node/npm
# are only needed to *fetch* it. The runtime stage is a bare debian with just
# the single binary + git, which drops node, npm, the npm cache, and the
# redundant CPU-baseline binary (~960MB single-stage -> ~340MB here).

# --- builder: use node/npm only to download the pinned platform binary -------
FROM node:22-slim AS builder

# Pin the exact opencode version. Do NOT use @latest so the image is
# reproducible and never silently upgrades.
ARG OPENCODE_VERSION=1.17.13

RUN npm install -g "opencode-ai@${OPENCODE_VERSION}"

# --- runtime: bare debian + the standalone binary ---------------------------
FROM debian:bookworm-slim

# git is used by opencode for repo context; ca-certificates for HTTPS to
# OpenRouter. bash is needed for the CMD.
RUN apt-get update \
    && apt-get install -y --no-install-recommends git ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# The npm `opencode` command is a direct symlink to this self-contained Bun
# executable — no node launcher is involved, so copying just the binary is
# enough to run it. (COPY resolves the symlink/hardlink to the real file.)
COPY --from=builder /usr/local/lib/node_modules/opencode-ai/bin/opencode.exe /usr/local/bin/opencode

# `opencode web` tries to open a browser via `xdg-open`, which does not exist
# in a headless container and throws on startup. A no-op shim makes the
# browser-open call succeed silently; the server keeps running.
RUN printf '#!/bin/sh\nexit 0\n' > /usr/local/bin/xdg-open \
    && chmod +x /usr/local/bin/xdg-open

# Belt-and-suspenders against auto-upgrade / version detection at startup.
# The config file sets "autoupdate": false; this env var disables it too.
ENV OPENCODE_DISABLE_AUTOUPDATE=true

# Global config path — autoupdate/model settings are only honored here.
COPY opencode.json /root/.config/opencode/opencode.json

COPY init.sh /init.sh
RUN chmod +x /init.sh

# Port the sandbox platform expects for web-served tools.
EXPOSE 8888

# init.sh writes the OpenRouter auth from OPENROUTER_API_KEY, then the web
# server binds all interfaces so it is reachable from outside the container.
ENTRYPOINT []
CMD ["/bin/bash", "-c", "/init.sh && opencode web --hostname 0.0.0.0 --port 8888"]
