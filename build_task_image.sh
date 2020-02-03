#!/bin/bash
cd "$(dirname "$0")"
set -e

TAG="latest"
IMAGE="johanhenriksson/pipeline-task:$TAG"

docker build --tag $IMAGE .

if [ "$1" == "--push" ]; then
    docker push $IMAGE
fi
