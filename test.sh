#!/bin/bash
cd "${0%/*}" || exit
set -e

# build
if [ "$1" == "--build" ]; then
    bash ./build.sh
fi

# -e TASK_CLUSTER="{\"type\":\"docker\"}" \
# -e TASK_DEFINITION="{\"id\":\"test\",\"name\":\"cowait.test\",\"image\":\"cowait/task\",\"inputs\":{\"folder\":\"./\"}}" \

# run tests
docker run \
    -v /var/run/docker.sock:/var/run/docker.sock \
    --workdir /var/cowait \
    cowait/task \
    python -m pytest
