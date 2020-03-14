#!/bin/bash
cd "${0%/*}" || exit
set -e

TAG="latest"
IMAGE="backtickse/task:$TAG"

docker build --tag $IMAGE .

if [ "$1" == "--push" ]; then
    docker push $IMAGE
fi
