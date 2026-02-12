#!/usr/bin/env bash

## Build Docker image for the R-Diff benchmark.
## The name of the Docker image is specified by the IMAGE file.
##
## Optional single-sample mode:
##   ./build.sh malicious/synthetic/libpng-1.6.43
##   MALICIOUS_SAMPLE=malicious/synthetic/libpng-1.6.43 ./build.sh


set -e

sample="${1:-${MALICIOUS_SAMPLE:-}}"

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

if [ -n "$sample" ]
then
    echo "Building single malicious sample: $sample"
    docker build --build-arg MALICIOUS_SAMPLE="$sample" -t $(cat IMAGE) .
else
    docker build -t $(cat IMAGE) .
fi
