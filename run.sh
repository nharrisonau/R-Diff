#!/usr/bin/env bash

## Run a Docker container with the R-Diff pipeline image.
## The name of the Docker image is specified by the IMAGE file.


set -e

docker run -ti --rm $(cat IMAGE)
