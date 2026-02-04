## Dockerfile for R-Diff.
FROM ubuntu:22.04

LABEL maintainer=""
LABEL description=""

RUN apt-get clean && apt-get update

# Copy the repo (Makefile, scripts, targets/, patches/, etc.)
WORKDIR /root/r-diff/
COPY targets/ .

RUN apt-get update && apt-get install -y \
    git wget \
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
 && rm -rf /var/lib/apt/lists/*

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y tclsh
# Build all target programs with all 3 variants (safe, backdoored, prev-safe).
RUN make all

# Collect samples (if present in repo root)
RUN chmod +x collect_samples.sh && ./collect_samples.sh
