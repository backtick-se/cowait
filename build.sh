#!/bin/bash
cd "${0%/*}" || exit
set -e

image="cowait/task"
version=$(grep 'VERSION.*=.*".*"' setup.py | sed -E 's/.*"(.*)"/\1/g')
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

# build dashboard
if [[ $* == *--with-dashboard* ]]; then
    (
    cd cloud
    yarn install
    yarn run build
    )
fi

# build image
echo "Building $image:$version"
docker build --tag "$image:latest" .

# tag versions
if [[ $* == *--tag* ]] || [[ $* == *--push* ]]; then
    echo "Tag: $image:$version"
    docker tag "$image:latest" "$image:$version"

    echo "Tag: $image:$minor"
    docker tag "$image:latest" "$image:$minor"
fi

# push versions
if [[ $* == *--push* ]]; then
    echo "Pushing: $image:latest"
    docker push "$image:latest"

    echo "Pushing: $image:$version"
    docker push "$image:$version"

    echo "Pushing: $image:$minor"
    docker push "$image:$minor"
fi
