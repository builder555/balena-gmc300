#!/bin/bash
set -e

BLOCK_NAME="balena-gmc300"

function build_and_push_image () {
  local BALENA_ARCH=$1
  local PLATFORM=$2

  TAG=$DOCKER_REPO/$BLOCK_NAME:$BALENA_ARCH-$VERSION

  echo "Building for $BALENA_ARCH, platform $PLATFORM, pushing to $TAG"
  
  docker buildx build . --pull \
      --build-arg BALENA_ARCH=$BALENA_ARCH \
      --platform $PLATFORM \
      --file Dockerfile.template \
      --tag $TAG --load

  echo "Publishing..."
  docker push $TAG
}

function create_and_push_manifest() {
  docker manifest create $DOCKER_REPO/$BLOCK_NAME:latest \
  --amend $DOCKER_REPO/$BLOCK_NAME:rpi-$VERSION

  docker manifest push --purge $DOCKER_REPO/$BLOCK_NAME:latest
}

DOCKER_REPO=${1:-builder555}
VERSION=${2:-$(<VERSION)}

build_and_push_image "rpi" "linux/arm/v6" 

create_and_push_manifest
