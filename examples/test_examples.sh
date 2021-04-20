#!/bin/bash

examples=$(find . -mindepth 1 -maxdepth 1 -type d)

for dir in $examples
do
    tests=$(find $dir -type f | grep 'test_.*\.py')
    if [ -z "$tests" ]; then
        echo "~~ No tests in $dir"
        continue
    fi

    # go into example folder
    echo "~~ Running tests in $dir"
    cd $dir

    # build
    cowait build

    # run tests
    cowait test --no-mount
    if [ "$?" != "0" ]; then
        echo "~~ Test failed in $dir"
        exit 1
    fi

    # move back to root
    cd ..
done
