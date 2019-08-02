#!/bin/bash

DOCKER_FILE=Dockerfile
DOCKER_REPO=pybbn37
DOCKER_TAG=local
APYBBN_VERSION=version
APYPI_REPO=repo

while getopts v:r: option
do
  case "${option}"
  in
  v) APYBBN_VERSION=${OPTARG};;
  r) APYPI_REPO=${OPTARG};;
esac
done

if [[ "version" == $APYBBN_VERSION ]]; then
  echo "version is required; -v"
elif [[ "repo" == $APYPI_REPO ]]; then
  echo "repo is required; -r"
else
  docker build --no-cache \
    -f $DOCKER_FILE \
    --build-arg APYBBN_VERSION=$APYBBN_VERSION \
    --build-arg APYPI_REPO=$APYPI_REPO \
    -t ${DOCKER_REPO}:${DOCKER_TAG} .
fi