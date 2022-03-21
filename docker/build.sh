#!/usr/bin/env bash

if [ "_$1" == "_" ]; then __red "please set volume root path."; exit 1; fi

IMAGE_NAME="spigot_ci"
CONTAINER_NAME="spigot"
path="$(readlink -f "$1")/Spigot"

function __mkdir() {
  mkdir -p "$1" > /dev/null 2>&1
}

function __green() {
  echo -e "\033[32m$1\033[0m"
}

function __red() {
  echo -e "\033[31m$1\033[0m"
}

function __verify() {
    if [ $? -eq 0 ]; then
      echo "$(__green 'success: ') $1"
    else
      echo "$(__red   ' failed: ') $1"
    fi
}

function __build() {
  docker rmi "$IMAGE_NAME:$1" > /dev/null 2>&1
  docker build -t "$IMAGE_NAME:$1" -f "JDK$1.dockerfile" empty > /dev/null
  __verify "build image $IMAGE_NAME:$1"
}

function __create() {
  ver="$1"
  jdk="$2"

  container="$CONTAINER_NAME-$ver"
  image="$IMAGE_NAME:$jdk"

  __mkdir "$path/$ver"

  docker rm "$container" > /dev/null 2>&1
  docker create --name "$container" \
  --env SHELL=sh \
  -v "$path/$ver:/output" \
  -v "$path/app:/app"
  "$image" "$ver" > /dev/null
  __verify "build container $container"
}

function __jdk8() {
  __build 8
  __create "1.16.5" 8
  __create "1.16.4" 8
  __create "1.16.3" 8
  __create "1.16.2" 8
  __create "1.16.1" 8
  __create "1.15.2" 8
  __create "1.15.1" 8
  __create "1.15"   8
  __create "1.14.4" 8
  __create "1.14.3" 8
  __create "1.14.2" 8
  __create "1.14.1" 8
  __create "1.14"   8
  __create "1.13.2" 8
  __create "1.13.1" 8
  __create "1.13"   8
  __create "1.12.2" 8
  __create "1.12.1" 8
  __create "1.12"   8
  __create "1.11.2" 8
  __create "1.11.1" 8
  __create "1.11"   8
  __create "1.10.2" 8
  __create "1.9.4"  8
  __create "1.9.2"  8
  __create "1.9"    8
  __create "1.8.8"  8
  __create "1.8.3"  8
  __create "1.8"    8
}

function __jdk16() {
  __build 16
  __create "1.17"   16
  __create "1.17.1" 16
}

function __jdk17() {
  __build 17
  __create "1.18"   17
  __create "1.18.1" 17
  __create "1.18.2" 17
}

__mkdir "$path/app"
__jdk8
__jdk16
__jdk17
