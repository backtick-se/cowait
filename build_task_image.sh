#!/bin/bash
cd "$(dirname "$0")"
set -e

TAG="base"
IMAGE="johanhenriksson/pipeline-task:$TAG"

docker build \
    --tag $IMAGE \
    --file ./worker/Dockerfile \
    .

docker push $IMAGE