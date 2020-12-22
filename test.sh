#!/bin/bash
cd "${0%/*}" || exit
set -e

build=0
examples=0
mark=""

while [ $# -gt 0 ]; do
    case "$1" in
        -b|--build)
            build=1
            shift
            ;;
        -m|--mark)
            shift
            if [ $# -gt 0 ]; then
                mark=$1
            else
                echo "no mark specified"
                exit 1
            fi
            shift
            ;;
        --examples)
            shift
            examples=1
            ;;
        *)
            echo "invalid parameter $1"
            exit 1
            ;;
    esac
done

# build
if [ $build -eq 1 ]; then
    bash ./build.sh
fi

if [ $examples -eq 1 ]; then
    # run example tests

    docker run \
        -v /var/run/docker.sock:/var/run/docker.sock \
        -v $(pwd)/examples:/var/task \
        cowait/task \
        bash ./test_examples.sh
else
    # run package tests
    cmd="pytest"
    extra_args=""

    # pytest mark filter
    if [ -n "$mark" ]; then
        cmd="$cmd -m $mark"
    fi

    # if the build flag is not set, mount the local directory
    if [ $build -eq 0 ]; then
        extra_args="-v $(pwd):/var/cowait"
    fi

    docker run $extra_args \
        -v /var/run/docker.sock:/var/run/docker.sock \
        --workdir /var/cowait \
        cowait/task \
        $cmd
fi
