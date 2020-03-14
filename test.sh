#!/bin/bash
dir=$(cd -P -- "$(dirname -- "$0")" && pwd -P)
set -e

# build
if [ "$1" == "--build" ]; then
    bash ./build.sh
fi

# -e TASK_CLUSTER="{\"type\":\"docker\"}" \
# -e TASK_DEFINITION="{\"id\":\"test\",\"name\":\"pipeline.test\",\"image\":\"backtickse/task\",\"inputs\":{\"folder\":\"./\"}}" \

# run tests
docker run \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -w /app \
    backtickse/task \
    python -m pytest
