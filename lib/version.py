"""
@File      : lib/version.py
@Author    : Skeleton_321
@CreateDate: 2022/2/22 8:55
by IntelliJ IDEA
"""
import json
import os.path

from lib import module
from lib import __root__


def get_init(path):
    def __init__(self, *args, **kwargs):
        persistence_path = f"{path}/{self.name()}.json"
        self.__persistence__ = {}
        if os.path.exists(persistence_path):
            with open(persistence_path, "r", encoding="utf-8") as fp:
                self.__persistence__ = json.load(fp)

    return __init__


def get_exit(path):
    def __exit__(self, exc_type, exc_val, exc_tb):
        persistence_path = f"{path}/{self.name()}.json"
        with open(persistence_path, "w", encoding="utf-8") as fp:
            json.dump(self.__persistence__, fp)

    return __exit__


def integer_version(path):
    @module.register("persistence")
    def decorator(cls):
        def write(self, version, value):
            self.__persistence__[version] = value

        def need_update(self, version, value):
            if version in self.__persistence__:
                return value > self.__persistence__[version]
            return True

        module.injection(cls, get_init(path), "__init__")
        module.injection(cls, get_exit(path), "__exit__")
        module.override(cls, write)
        module.override(cls, need_update)

    return decorator


def string_version(path):
    if path[:2] == './':
        path = f"{__root__}/{path[2:]}"

    @module.register("persistence")
    def decorator(cls):
        def write(self, version, value):
            if version not in self.__persistence__:
                self.__persistence__[version] = []
            self.__persistence__[version].append(value)

        def need_update(self, version, value):
            if version in self.__persistence__:
                return value not in self.__persistence__[version]
            return True

        module.injection(cls, get_init(path), "__init__")
        module.injection(cls, get_exit(path), "__exit__")
        module.override(cls, write)
        module.override(cls, need_update)

    return decorator
