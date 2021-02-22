#!/bin/bash
cd "${0%/*}" || exit
set -e

image="cowait/task"
notebook="cowait/notebook"
version=$(grep 'version.*=.*".*"' cowait/version.py | sed -E 's/.*"(.*)"/\1/g')
minor=$(echo $version | sed -E 's/([0-9]+\.[0-9]+)\.[0-9]+/\1/g')

if [ -n "$GITHUB_REF" ]; then
    # we are running in a github action
    # ensure tag version matches python package version!
    github_version=${GITHUB_REF/refs\/tags\//}
    if [ "$version" != "$github_version" ]; then
        echo "Version missmatch between package ($version) and git tag ($github_version)"
        exit 1
    fi
fi

args=$*

# build dashboard
if [[ $args == *--with-dashboard* ]]; then
    (
    cd cloud
    yarn install
    yarn run build
    )
fi


build() {
    # build image
    echo "Building $1:$version"
    docker build --tag "$1:latest" $2

    # tag versions
    if [[ $args == *--tag* ]] || [[ $args == *--push* ]]; then
        echo "Tag: $1:$version"
        docker tag "$1:latest" "$1:$version"

        echo "Tag: $1:$minor"
        docker tag "$1:latest" "$1:$minor"
    fi

    # push versions
    if [[ $args == *--push* ]]; then
        echo "Pushing: $1:latest"
        docker push "$1:latest"

        echo "Pushing: $1:$version"
        docker push "$1:$version"

        echo "Pushing: $1:$minor"
        docker push "$1:$minor"
    fi
}

build $image .

if [[ $args == *--with-notebook* ]]; then
    (
    build $notebook ./images/notebook
    )
fi

