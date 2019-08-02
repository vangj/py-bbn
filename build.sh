#!/bin/bash

DOCKER_FILE=Dockerfile
DOCKER_REPO=pybbn37
DOCKER_TAG=local

docker build --no-cache \
    -f $DOCKER_FILE \
    --build-arg APYBBN_VERSION=0.2.4 \
    --build-arg APYPI_REPO=testpypi \
    -t ${DOCKER_REPO}:${DOCKER_TAG} .