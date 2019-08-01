#!/bin/bash

DOCKER_FILE=Dockerfile-3.7
REPO=pybbn37
TAG=local

docker build --no-cache -f $DOCKER_FILE -t $REPO:$TAG .