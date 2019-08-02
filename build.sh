#!/bin/bash

DOCKER_FILE=Dockerfile
DOCKER_REPO=pybbn37
DOCKER_TAG=local

docker build --no-cache \
    -f $DOCKER_FILE \
    --build-arg PYBBN_VERSION=0.2.3 \
    --build-arg PYPI_REPO=testpypi \
    -t ${DOCKER_REPO}:${DOCKER_TAG} .