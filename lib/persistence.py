"""
@File      : src/client/persistence.py
@Author    : Skeleton_321
@CreateDate: 2022/2/5 21:53
by IntelliJ IDEA
"""
from __future__ import annotations

import datetime
import json
import logging
import os.path

from . import log


class PersistenceManager:
    def __init__(self, path):
        self.path = path
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as fp:
                self.__persistence__ = json.load(fp)
        else:
            self.__persistence__ = {}

    def get(self, key, default: int | str | list = 0):
        if key not in self.__persistence__:
            self.__persistence__[key] = default
        return self.__persistence__[key]

    def is_skipped(self, key, value, default: int | str | list = 0):
        if (t := type(self.get(key, default))) == list:
            return value in self.__persistence__[key]
        elif t == int:
            return value <= self.__persistence__[key]
        return value == self.__persistence__[key]

    def set(self, key, value):
        self.__persistence__[key] = value

    def append(self, key, value):
        self.get(key, [])
        self.__persistence__[key].append(value)

    def save(self):
        with open(self.path, "w", encoding="utf-8") as fp:
            json.dump(self.__persistence__, fp)


class ResourceManager:
    def __init__(self, name: str, level=logging.INFO, persistence=None):
        self.name = name.lower()
        path_list = [f"./tmp/{name}", "./config", "./auth", f"./log/{name}"]
        for p in path_list:
            if not os.path.exists(p):
                os.makedirs(p)

        persistence = persistence if persistence is not None else PersistenceManager

        self.workspace = path_list[0]
        self.config = persistence(f"./config/{self.name}.json")
        with open(f"{path_list[2]}/token", "r", encoding="utf-8") as fp:
            lines = fp.readlines()
            self.token = "".join(lines if len(lines) < 2 else lines[1:-1])
        self.log = log.init(name, f'{path_list[3]}/{datetime.datetime.now().strftime("%Y-%m-%d")}', level)

    def join_path(self, filename):
        return f"{self.workspace}/{filename}"
