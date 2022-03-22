#!/usr/bin/env bash

if [ "_$1" == "_" ]; then __red "please set volume root path."; exit 1; fi

IMAGE_NAME="spigot_ci"
CONTAINER_NAME="spigot"
DEPENDS_ON_JDK8=(
"1.16.5"
"1.16.4"
"1.16.3"
"1.16.2"
"1.16.1"
"1.15.2"
"1.15.1"
"1.15"
"1.14.4"
"1.14.3"
"1.14.2"
"1.14.1"
"1.14"
"1.13.2"
"1.13.1"
"1.13"
"1.12.2"
"1.12.1"
"1.12"
"1.11.2"
"1.11.1"
"1.11"
"1.10.2"
"1.9.4"
"1.9.2"
"1.9"
"1.8.8"
"1.8.3"
"1.8"
)
DEPENDS_ON_JDK16=(
"1.17.1"
"1.17"
)
DEPENDS_ON_JDK17=(
"1.18.2"
"1.18.1"
"1.18"
)

function __mkdir() {
  mkdir -p "$1" > /dev/null 2>&1
}

function __verify() {
    if [ $? -eq 0 ]; then
      echo -e "\033[32m success\033[0m: $1"
    else
      echo -e "\031[31m failed \033[0m: $1"
    fi
    return $?
}

function __docker_rmi() {
  docker rmi "$IMAGE_NAME:$1" > /dev/null 2>&1
}

function __docker_rm() {
    docker rm "$CONTAINER_NAME-$1" > /dev/null 2>&1
}

function __status() {
  if status=$(docker inspect --format '{{.State.Status}}' "$1" 2>&1); then echo "$status"; return 0;
  else echo "not exists"; return 1;
  fi
}

function __build() {
  docker build -t "$IMAGE_NAME:$1" -f "JDK$1.dockerfile" empty > /dev/null
  __verify "构建镜像 $IMAGE_NAME:$1"
}

function __create() {
  ver="$1"
  jdk="$2"

  container="$CONTAINER_NAME-$ver"
  image="$IMAGE_NAME:$jdk"

  __mkdir "$path/$ver"
  if __status "$container" > /dev/null; then echo "skip   : 构建容器 $container"; return 0; fi
  docker create --name "$container" \
  --env SHELL=sh \
  -v "$path/$ver:/output" \
  "$image" "$ver" > /dev/null
  __verify "构建容器 $container"
}

function remove_all() {
  for v in "${DEPENDS_ON_JDK8[@]}"  ; do __docker_rm "$v"; done
  __docker_rmi 8
  for v in "${DEPENDS_ON_JDK16[@]}" ; do __docker_rm "$v"; done
  __docker_rmi 16
  for v in "${DEPENDS_ON_JDK17[@]}" ; do __docker_rm "$v"; done
  __docker_rmi 17
}

function update() {
  __build 8
  __build 16
  __build 17
  for v in "${DEPENDS_ON_JDK8[@]}"  ; do __create "$v" 8 ; done
  for v in "${DEPENDS_ON_JDK16[@]}" ; do __create "$v" 16; done
  for v in "${DEPENDS_ON_JDK17[@]}" ; do __create "$v" 17; done
}

function help() {
  echo "$0 [[--update|--rebuild|--remove] [输出文件夹根目录] | --help|-h]"
  echo "--update:   创建还未创建的容器和镜像"
  echo "--rebuild:  移除所有容器和镜像并重新创建"
  echo "--remove:   移除所有容器和镜像"
  echo "--help, -h: 帮助信息"
}

path="$HOME/tmp"

for arg in "$@"; do
  case "$arg" in
  "--rebuild") need_update=1; need_remove=1 ;;
  "--update")  need_update=1 ;;
  "--remove")  need_remove=1 ;;
  "--help")    help ;;
  "-h")        help ;;
  "*")         test -e "$arg"; __verify "对路径 '$arg' 的检查." && path="$arg" || exit 1
  esac
done

path="$(readlink -f "$path")/Spigot"

__mkdir "$path"
if [ ${need_remove:-0} -eq 1 ]; then remove_all; fi
if [ ${need_update:-0} -eq 1 ]; then update; fi
