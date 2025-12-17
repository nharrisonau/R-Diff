## Dockerfile for ROSARUM.
FROM ubuntu:22.04

LABEL maintainer="dimitri.kokkonis@cea.fr"
LABEL description="Docker image for the ROSARUM backdoor detection benchmark"

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

WORKDIR /root/rosarum/

# Copy the repo (Makefile, scripts, targets/, patches/, etc.)
COPY . .

RUN apt-get update && apt-get install -y --no-install-recommends \
    tzdata \
    \
    # Base
    ca-certificates \
    curl \
    wget \
    \
    # Build essentials
    build-essential \
    cmake \
    pkg-config \
    \
    # Autotools / build tooling
    autoconf \
    autogen \
    automake \
    libtool \
    patch \
    \
    # Parsers / generators
    bison \
    flex \
    re2c \
    \
    # Toolchains / compilers
    clang \
    gcc-multilib \
    g++-multilib \
    \
    # VCS / fetch helpers (OpenWrt buildroot often expects these)
    git \
    subversion \
    \
    # Scripting / language runtime needed by various targets
    perl \
    python3 \
    python3-distutils \
    python3-setuptools \
    tclsh \
    swig \
    \
    # Archivers / utilities
    file \
    rsync \
    unzip \
    xz-utils \
    zip \
    \
    # Build UI / config libs
    libncurses5-dev \
    \
    # Crypto / compression fundamentals
    libssl-dev \
    libelf-dev \
    zlib1g-dev \
    libz-dev \
    \
    # Networking utility (used in some targets)
    netcat-traditional \
    \
    # Media / audio deps (libsndfile etc.)
    libasound2-dev \
    libflac-dev \
    libmp3lame-dev \
    libmpg123-dev \
    libogg-dev \
    libopus-dev \
    libvorbis-dev \
    \
    # Image / document deps (libpng/libtiff/poppler stack)
    libbrotli-dev \
    libbz2-dev \
    libdeflate-dev \
    libharfbuzz-dev \
    libjbig-dev \
    libjpeg-dev \
    liblerc-dev \
    liblcms2-dev \
    liblzma-dev \
    libopenjp2-7-dev \
    libtiff-dev \
    libwebp-dev \
    libzstd-dev \
    \
    # Auth / system / misc
    libcap-dev \
    libpam-dev \
    \
    # Data / parsing libs
    libsqlite3-dev \
    libxml2-dev \
    gawk \
    gettext \
 && ln -fs /usr/share/zoneinfo/$TZ /etc/localtime \
 && dpkg-reconfigure -f noninteractive tzdata \
 && rm -rf /var/lib/apt/lists/*

# Build all target programs with all 3 variants (safe, backdoored, prev-safe).
# RUN make all

# Collect samples (if present in repo root)
# RUN chmod +x collect_samples.sh && ./collect_samples.sh
