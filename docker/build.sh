#!/bin/bash
#clear;clear

v="$1"

if [ ${#v} -eq 0 ]; then
    echo "please set java version."
    exit 127
elif [ "$v" == "8" ] || [ "$v" == "16" ] || [ "$v" == "17" ]; then
    NAME="spigot_jdk$v"
    echo "target: $NAME"
else
    echo "java version must be 8, 16 or 17."
    exit 126
fi

unset v

# build and create
docker build -t sync/"$NAME" -f "$NAME"/Dockerfile . \
&& \
docker create --name sync_"$NAME" \
--env SUBMIT_URL="$SUBMIT_URL" \
--env SHELL=sh \
-v /home/sync/auth:/workspace/auth:ro \
-v /home/sync/log:/workspace/log \
-v /home/sync/lib:/workspace/lib:ro \
-v /home/sync/tmp:/workspace/tmp \
-v /home/sync/config:/workspace/config \
sync/"$NAME"

if [ $? -eq 0 ]; then
    echo "build successful."
    echo "run with \"docker start sync_$NAME && docker attach sync_$NAME\""
fi

exit $?
