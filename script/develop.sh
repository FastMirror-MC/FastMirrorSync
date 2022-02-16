#!/bin/sh

ln -s client src
cd src || exit
ln -s ../lib lib
ln -s ../docker/spigot_jdk8 spigot_jdk8
ln -s ../docker/spigot_jdk16 spigot_jdk16
ln -s ../docker/spigot_jdk17 spigot_jdk17
ln ../docker/sync.py spigot.py
ln ../docker/info.py info.py
