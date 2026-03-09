#!/usr/bin/env bash

## Build Docker image for the R-Diff pipeline.
## The name of the Docker image is specified by the IMAGE file.
##
## Optional single-sample mode:
##   ./build.sh synthetic/libpng-1.6.43
##   TARGET_SAMPLE=synthetic/libpng-1.6.43 ./build.sh


set -e

sample="${1:-${TARGET_SAMPLE:-}}"

# The command `git submodule status --recursive` displays the list of registered submodules in the current
# repo. If a submodule is not cloned/uninitialized, its corresponding line in the command's output
# is prefixed with a '-'. So, by looking at the first byte, we can tell if any submodule is not
# cloned and stop the build.
status_list=$(git submodule status --recursive | cut -b 1)
for status in $status_list
do
    if [ "$status" == "-" ]
    then
        echo "At least one submodule is uninitialized; stopping build." 1>&2
        echo "Run \`git submodule update --init --recursive\` at the root of the repo." 1>&2
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
