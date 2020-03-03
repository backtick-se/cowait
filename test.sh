#!/bin/bash
cd "${0%/*}" || exit
set -e

# build
if [ "$1" == "--build" ]; then
    bash build.sh
fi

# run tests
docker run \
    -v /var/run/docker.sock:/var/run/docker.sock \
    docker.backtick.se/task \
    python -m pytest
