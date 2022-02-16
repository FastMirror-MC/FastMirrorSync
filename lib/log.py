"""
@File      : src/client/log.py
@Author    : Skeleton_321
@CreateDate: 2022/2/5 21:52
by IntelliJ IDEA
"""
import datetime
import logging
import sys

import requests

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOGGER_FORMAT = "{asctime}.{msecs:03.0f} {levelname:>8} --- [{module:>16}:{lineno:>03}]: {message}"


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


def init(name, path, level):
    requests.packages.urllib3.disable_warnings()
    logging.basicConfig(level=logging.DEBUG, format=LOGGER_FORMAT, style="{", datefmt=DATE_FORMAT, handlers={
        get_file_handler(f'{path}.log', logging.INFO),
        get_file_handler(f'{path}-debug.log', logging.DEBUG),
        get_stream_handler()
    })
    log = logging.getLogger(name)
    log.setLevel(level)
    return log
