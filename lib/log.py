"""
@File      : lib/log.py
@Author    : Skeleton_321
@CreateDate: 2022/2/22 9:12
by IntelliJ IDEA
"""
import datetime
import logging
import sys

# import requests

from lib import module

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOGGER_FORMAT = "{asctime}.{msecs:03.0f} {name} {levelname:>8} --- [{module:>16}:{lineno:>03}]: {message}"


def get_file_handler(filename, level):
    tmp = logging.FileHandler(filename, mode="w", encoding="utf-8")
    tmp.setFormatter(logging.Formatter(fmt=LOGGER_FORMAT, datefmt=DATE_FORMAT, style="{"))
    tmp.setLevel(level=level)
    return tmp


def get_stream_handler():
    tmp = logging.StreamHandler(stream=sys.stderr)
    tmp.setFormatter(logging.Formatter(fmt=LOGGER_FORMAT, datefmt=DATE_FORMAT, style="{"))
    tmp.setLevel(logging.INFO)
    return tmp


def get_logger(name, level):
    # requests.packages.urllib3.disable_warnings()
    path = datetime.datetime.now().strftime("%Y-%m-%d")
    logging.basicConfig(level=logging.DEBUG, format=LOGGER_FORMAT, style="{", datefmt=DATE_FORMAT, handlers={
        get_file_handler(f'./log/{path}.log', logging.INFO),
        get_file_handler(f'./log/{path}-debug.log', logging.DEBUG),
        get_stream_handler()
    })
    log = logging.getLogger(name)
    log.setLevel(level)
    return log


global_log = get_logger("global", logging.INFO)

debug = global_log.debug
info = global_log.info
warning = global_log.warning
error = global_log.error
exception = global_log.exception
critical = global_log.critical


@module.register("logger")
def logger(cls):
    def __init__(self, *args, **kwargs):
        self.__logger__inst__ = get_logger(self.name(), logging.INFO)
        self.debug = self.__logger__inst__.debug
        self.info = self.__logger__inst__.info
        self.warning = self.__logger__inst__.warning
        self.error = self.__logger__inst__.error
        self.exception = self.__logger__inst__.exception
        self.critical = self.__logger__inst__.critical

    module.injection(cls, __init__)
