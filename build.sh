#!/usr/bin/env bash

## Build Docker image for the R-Diff pipeline.
## The name of the Docker image is specified by the IMAGE file.
##
## Optional single-sample mode:
##   ./build.sh synthetic/libpng-1.6.43
##   TARGET_SAMPLE=synthetic/libpng-1.6.43 ./build.sh


set -e

sample="${1:-${TARGET_SAMPLE:-}}"

# `git submodule status` lists the top-level submodules, which are exactly the per-target
# original/ and previous/ source trees the pipeline builds from. An uninitialized one is
# prefixed with '-', so checking the first byte tells us whether a source tree is missing.
#
# Deliberately NOT --recursive. Upstream projects declare their own nested submodules
# (openssl alone pulls in tlsfuzzer, cloudflare-quiche, fuzz/corpora, ...), and the set
# varies by release tag, so re-pinning a target to a newer version can introduce dozens of
# uninitialized nested entries. None of them are ever built: every Makefile resolves its
# source with `git -C <repo> archive <tag>`, and git archive emits an empty directory entry
# for a gitlink rather than its contents. Requiring them would mean cloning gigabytes of
# upstream test corpora to no effect.
status_list=$(git submodule status | cut -b 1)
for status in $status_list
do
    if [ "$status" == "-" ]
    then
        echo "At least one target source tree is uninitialized; stopping build." 1>&2
        echo "Run \`git submodule update --init\` at the root of the repo." 1>&2
        exit 1
    fi
done

if [ -n "$sample" ]
then
    echo "Building single sample: $sample"
    docker build --build-arg TARGET_SAMPLE="$sample" -t $(cat IMAGE) .
else
    docker build -t $(cat IMAGE) .
fi
