#!/usr/bin/env bash

# docker hub username
USERNAME=dockreg.lebanon.cd-adapco.com:5000
# image name
IMAGE=flaskfunc

usage()
{
    echo "usage: ./release.sh [ [-p | --patch] | [-m | --minor] | [-v | --version]]"
    echo " bumps version by patch, minor, or major version number"
}

op=""
while [ "$1" != "" ]; do
    case $1 in
        -p | --patch )          op="patch"
                                ;;
        -m | --minor )          op="minor"
                                ;;
        -v | --version )        op="major"
                                ;;
        * )                     ;;
    esac
    shift
done

if [ "$op" = "" ]; then
	usage
	exit
fi

echo "creating new $op version"

set -ex


# ensure we're up to date
git pull

# bump version
docker run --rm -v "$PWD":/app treeder/bump $op
version=`cat VERSION`
echo "version: $version"

# run build
./build.sh

# tag it
git add -A
git commit -m "version $version"
git tag -a "$version" -m "version $version"
git push
git push --tags
docker tag $USERNAME/$IMAGE:latest $USERNAME/$IMAGE:$version

# push it
docker push $USERNAME/$IMAGE:latest
docker push $USERNAME/$IMAGE:$version
