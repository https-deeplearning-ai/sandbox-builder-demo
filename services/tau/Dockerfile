# tau: Hugging Face's terminal coding agent (pip package `tau-ai`), pinned to a
# fixed version. Default provider is OpenRouter (model GLM-5.2); the OpenRouter
# key is read at runtime from OPENROUTER_API_KEY, so no interactive `/login` is
# needed — tau's provider layer falls back to the api_key_env automatically.
#
# Two-stage build on Alpine: tau-ai is pure Python with prebuilt wheels for all
# deps (pydantic-core ships musllinux wheels), so nothing compiles. The builder
# uses `uv` to assemble a lean venv (no pip/setuptools inside it); the runtime
# is a bare python-alpine + git that just carries that venv. This keeps the
# image around ~120MB vs. ~220MB for a single-stage python:3.12-slim install.

# --- builder: assemble a self-contained venv with uv -------------------------
FROM python:3.12-alpine AS builder

# Pin the exact tau version. Do NOT use an unpinned spec so the image is
# reproducible and never silently upgrades.
ARG TAU_VERSION=0.1.2

# Copy the standalone uv binary from its official image — no pip bootstrap.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Use the Alpine system CPython (musl); never fetch a managed glibc build that
# could not run on musl at runtime.
ENV UV_PYTHON_DOWNLOADS=never

# `uv venv` creates a venv WITHOUT pip/setuptools, so the copied tree stays
# minimal. --no-cache avoids leaving a wheel cache in the layer.
RUN uv venv /opt/venv --python 3.12 \
    && uv pip install --python /opt/venv/bin/python --no-cache "tau-ai==${TAU_VERSION}"

# --- runtime: bare python-alpine + the venv ----------------------------------
FROM python:3.12-alpine

# git: used by the coding agent for repo context. ca-certificates: HTTPS to
# OpenRouter. ttyd + bash: serve tau's terminal UI over the web on a port, the
# way the sandbox platform expects (matches utils-ttyd / utils-opencode-web).
RUN apk add --no-cache git ca-certificates ttyd bash

# The venv's interpreter symlinks to /usr/local/bin/python3.12, which exists in
# this identical base image, so the venv runs as-is.
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Default OpenRouter model. Override at build with --build-arg TAU_MODEL=...;
# override per-run with `tau -m <model>`.
ARG TAU_MODEL=z-ai/glm-5.2

# Make OpenRouter the default provider/model without an interactive `/login`, by
# generating ~/.tau/providers.json from the pinned library itself so the file is
# always valid for exactly this tau version. The API key is supplied at runtime
# via OPENROUTER_API_KEY, which tau's provider layer reads as a fallback.
RUN mkdir -p /root/.tau \
    && python -c "import json; from tau_coding.provider_config import ProviderSettings, set_default_provider_model; \
open('/root/.tau/providers.json','w').write(json.dumps(set_default_provider_model(ProviderSettings(), provider_name='openrouter', model='${TAU_MODEL}').to_json(), indent=2) + '\n')"

# Silence tau's startup PyPI update check — the version is pinned on purpose.
ENV TAU_NO_UPDATE_CHECK=1

# Port the sandbox platform expects for web-served tools.
EXPOSE 8888

# Serve tau's interactive TUI over the web on port 8888 via ttyd. ttyd spawns
# tau in a PTY and inherits the container env, so OPENROUTER_API_KEY (supplied
# at `docker run` time) reaches tau. -W makes the web client writable.
CMD ["ttyd", "-p", "8888", "-W", "tau"]
