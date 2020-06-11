#!/bin/bash
cd "${0%/*}" || exit
set -e

# build
if [[ $* == *--build* ]]; then
    bash ./build.sh
fi

# run package tests
docker run \
    -v /var/run/docker.sock:/var/run/docker.sock \
    --workdir /var/cowait \
    cowait/task \
    python -m pytest

# run example tests
if [[ $* == *--examples* ]]; then
    docker run \
        -v /var/run/docker.sock:/var/run/docker.sock \
        -v $(pwd)/examples:/var/task \
        cowait/task \
        bash ./test_examples.sh
fi