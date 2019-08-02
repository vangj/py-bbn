#!/bin/bash

DOCKER_FILE=Dockerfile-2.7
DOCKER_REPO=pybbn27
DOCKER_TAG=local

docker build --no-cache \
    -f $DOCKER_FILE \
    -t ${DOCKER_REPO}:${DOCKER_TAG} .