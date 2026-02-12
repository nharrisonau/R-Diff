## Dockerfile for R-Diff.
FROM ubuntu:22.04

LABEL maintainer=""
LABEL description=""

WORKDIR /root/r-diff/
ARG DEBIAN_FRONTEND=noninteractive
ARG MALICIOUS_SAMPLE=""

# Install deps first so Docker can cache the heavy apt layer across code changes.
# We clear apt lists first and retry once to dodge occasional mirror races (404 during install).
RUN set -eux; \
    packages=" \
        ca-certificates \
        git wget \
        file patch tar \
        libncurses-dev ncurses-base ncurses-bin \
        autoconf autogen automake bison build-essential cmake \
        binutils bzip2 diffutils findutils flex gawk util-linux grep coreutils \
        libc6-dev zlib1g-dev \
        make perl python3 rsync subversion unzip debianutils \
        libasound2-dev libboost-all-dev libbrotli-dev libbz2-dev libcap-dev libdeflate-dev \
        libflac-dev libharfbuzz-dev libjbig-dev libjpeg-dev liblerc-dev liblcms2-dev liblzma-dev \
        libmp3lame-dev libmpg123-dev libogg-dev libopenjp2-7-dev libopus-dev libpam-dev \
        libsqlite3-dev libssl-dev libtiff-dev libtool libvorbis-dev libwebp-dev libxml2-dev \
        libzstd-dev netcat-traditional pkg-config re2c zip \
        tclsh \
    "; \
    rm -rf /var/lib/apt/lists/*; \
    apt-get update -o Acquire::Retries=5 -o Acquire::http::No-Cache=True; \
    if ! apt-get install -y --no-install-recommends $packages; then \
        rm -rf /var/lib/apt/lists/*; \
        apt-get update -o Acquire::Retries=5 -o Acquire::http::No-Cache=True; \
        apt-get install -y --no-install-recommends $packages; \
    fi; \
    rm -rf /var/lib/apt/lists/*

# Copy the full repo (including .git) so baseline scripts can enumerate tags.
COPY . .

# Build all targets by default, or one malicious sample when MALICIOUS_SAMPLE is set.
RUN set -eux; \
    if [ -n "${MALICIOUS_SAMPLE}" ]; then \
        python3 -c "import json, pathlib, os; sample=os.environ['MALICIOUS_SAMPLE']; p=pathlib.Path('targets/malicious/baselines_config.json'); entries=json.loads(p.read_text()); subset=[e for e in entries if e.get('path')==sample]; assert subset, f'Unknown malicious sample: {sample}'; pathlib.Path('/tmp/baselines_config.single.json').write_text(json.dumps(subset, indent=2)); print(f'Using single-sample config for {sample}')" ; \
        make -C "targets/${MALICIOUS_SAMPLE}" SUDO=; \
        python3 targets/malicious/scripts/build_baselines.py --config /tmp/baselines_config.single.json --out /tmp/baselines.single.csv; \
        python3 targets/malicious/scripts/collect_outputs_v2.py --repo-root /root/r-diff --out-base /root/r-diff/outputs --config /tmp/baselines_config.single.json --baselines /tmp/baselines.single.csv; \
    else \
        make -C targets all; \
        chmod +x targets/collect_samples.sh && targets/collect_samples.sh; \
    fi
