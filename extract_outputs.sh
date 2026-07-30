#!/usr/bin/env bash

## Copy collected outputs out of the R-Diff pipeline image onto the host.
## The pipeline builds and collects inside the image (see the RUN step in the
## Dockerfile), so the binaries sit in an image layer until they are copied out.
## run.sh does not do this: it starts a throwaway interactive container.
##
## Usage:
##   ./extract_outputs.sh              # -> ./outputs
##   ./extract_outputs.sh /some/where  # -> /some/where
##
## Copying into an existing directory accumulates samples rather than replacing
## them, which is what per-sample builds need: each `./build.sh <sample>` retags
## the same image, and that image holds only the most recent sample's outputs.

set -e

dest="${1:-outputs}"
image="$(cat IMAGE)"

mkdir -p "$dest"

cid="$(docker create "$image")"
trap 'docker rm -f "$cid" >/dev/null 2>&1 || true' EXIT
docker cp "$cid:/root/r-diff/outputs/." "$dest/"

echo "extracted to $dest"
for flavor in normal stripped; do
    n=$(ls -d "$dest"/targets/"$flavor"/*/* 2>/dev/null | wc -l)
    echo "  $flavor: $n sample dirs"
done
