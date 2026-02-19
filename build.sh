#!/usr/bin/env bash

## Build Docker image for the R-Diff benchmark.
## The name of the Docker image is specified by the IMAGE file.
##
## Optional single-sample mode:
##   ./build.sh synthetic/libpng-1.6.43
##   TARGET_SAMPLE=synthetic/libpng-1.6.43 ./build.sh
##
## Baseline limiting:
##   default: immediate previous only (BASELINE_LIMIT=1)
##   BASELINE_LIMIT=0 ./build.sh   # build full configured history


set -e

sample="${1:-${TARGET_SAMPLE:-}}"
baseline_limit="${BASELINE_LIMIT:-}"

# The command `git submodule status` displays the list of registered submodules in the current
# repo. If a submodule is not cloned/uninitialized, its corresponding line in the command's output
# is prefixed with a '-'. So, by looking at the first byte, we can tell if any submodule is not
# cloned and stop the build.
status_list=$(git submodule status | cut -b 1)
for status in $status_list
do
    if [ "$status" == "-" ]
    then
        echo "At least one submodule is uninitialized; stopping build." 1>&2
        echo "Run \`git submodule update --init\` at the root of the repo." 1>&2
        exit 1
    fi
done

build_args=()
if [ -n "$baseline_limit" ]
then
    build_args+=(--build-arg BASELINE_LIMIT="$baseline_limit")
fi

if [ -n "$sample" ]
then
    echo "Building single sample: $sample"
    docker build "${build_args[@]}" --build-arg TARGET_SAMPLE="$sample" -t $(cat IMAGE) .
else
    docker build "${build_args[@]}" -t $(cat IMAGE) .
fi
