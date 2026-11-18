# ttyd: a general-purpose Python 3.14 web terminal. ttyd serves a writable bash
# shell on port 8888, the way the sandbox platform expects for web-served tools
# (matches services/tau and services/opencode-web).
#
# Base is the official python:3.14-slim image, which is Debian (trixie), so
# system packages come from apt. The shell runs as a non-root user that has
# passwordless sudo, so `sudo apt-get install <pkg>` works from the terminal.

FROM python:3.14-slim

# Non-root login user for the web terminal. Override at build time with
# --build-arg SANDBOX_USER=... / SANDBOX_UID=...
ARG SANDBOX_USER=user
ARG SANDBOX_UID=1000

# sudo: privilege escalation for the non-root user. tini: PID 1 that reaps the
# shells ttyd leaves behind. ca-certificates/curl/git: baseline tools for pip,
# HTTPS and repo work.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        sudo tini bash ca-certificates curl git \
    && rm -rf /var/lib/apt/lists/*

# Debian trixie does not package ttyd, so install the static binary from the
# upstream GitHub release. The version is pinned and each architecture's
# binary is verified against its published SHA-256, so the image is
# reproducible and a tampered or truncated download fails the build.
ARG TTYD_VERSION=1.7.7
ARG TTYD_SHA256_AMD64=8a217c968aba172e0dbf3f34447218dc015bc4d5e59bf51db2f2cd12b7be4f55
ARG TTYD_SHA256_ARM64=b38acadd89d1d396a0f5649aa52c539edbad07f4bc7348b27b4f4b7219dd4165
ARG TARGETARCH
RUN case "${TARGETARCH}" in \
        amd64) ttyd_arch=x86_64;  ttyd_sha="${TTYD_SHA256_AMD64}" ;; \
        arm64) ttyd_arch=aarch64; ttyd_sha="${TTYD_SHA256_ARM64}" ;; \
        *) echo "unsupported architecture: ${TARGETARCH}" >&2; exit 1 ;; \
    esac \
    && curl -fsSL -o /usr/local/bin/ttyd \
        "https://github.com/tsl0922/ttyd/releases/download/${TTYD_VERSION}/ttyd.${ttyd_arch}" \
    && echo "${ttyd_sha}  /usr/local/bin/ttyd" | sha256sum -c - \
    && chmod 0755 /usr/local/bin/ttyd

# Create the user and grant passwordless sudo through a drop-in that visudo
# validates, so a malformed rule fails the build instead of breaking sudo.
RUN useradd --create-home --shell /bin/bash --uid "${SANDBOX_UID}" "${SANDBOX_USER}" \
    && echo "${SANDBOX_USER} ALL=(ALL) NOPASSWD:ALL" > "/etc/sudoers.d/${SANDBOX_USER}" \
    && chmod 0440 "/etc/sudoers.d/${SANDBOX_USER}" \
    && visudo -cf "/etc/sudoers.d/${SANDBOX_USER}"

# pip as a non-root user installs into ~/.local, so its scripts must be on PATH
# for installed CLIs to run without sudo. ENV covers non-login shells
# (`docker exec`). The login shell ttyd starts resets PATH in /etc/profile, and
# Debian's ~/.profile re-adds ~/.local/bin only if the directory already exists
# at login, so it is created below; otherwise the first `pip install` in a
# session would produce commands that are not found until re-login.
ENV PATH="/home/${SANDBOX_USER}/.local/bin:${PATH}"

USER ${SANDBOX_USER}
WORKDIR /home/${SANDBOX_USER}
RUN mkdir -p "/home/${SANDBOX_USER}/.local/bin"

# Port the sandbox platform expects for web-served tools.
EXPOSE 8888

# -p 8888 binds all interfaces on 8888; -W makes the web client writable
# (ttyd is read-only by default). A login shell picks up the user's profile.
ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["ttyd", "-p", "8888", "-W", "bash", "-l"]
