#!/bin/bash

DOCKER_FILE=Dockerfile-2.7
REPO=pybbn27
TAG=local

docker build --no-cache -f $DOCKER_FILE -t $REPO:$TAG .