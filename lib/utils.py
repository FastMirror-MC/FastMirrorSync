"""
@File      : lib/utils.py
@Author    : Skeleton_321
@CreateDate: 2022/2/22 8:39
by IntelliJ IDEA
"""
from __future__ import annotations

import atexit
import datetime
import hashlib
import sys
import time
import traceback

import pytz

from lib import log

__all__ = ["datetime2str", "get_checksum", "if_file_invalid", "get_mills_time", "register_exit_event"]
exit_event_queue = []


def datetime2str(dt: datetime.datetime):
    return dt.astimezone(pytz.UTC).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def get_checksum(stream, mode: str = "sha1"):
    stream.seek(0, 0)
    if mode == "sha1":
        invoke = hashlib.sha1()
    elif mode == "sha256":
        invoke = hashlib.sha256()
    else:
        invoke = hashlib.md5()
    invoke.update(stream.read())
    return str(invoke.hexdigest()).lower()


def if_file_invalid(stream, checksum: str, mode: str):
    if checksum is None:
        log.warning("need origin checksum. skipped.")
        return False
    return checksum.lower() != get_checksum(stream, mode)


def get_mills_time():
    return int(time.time() * 1000)


def register_exit_event(func):
    exit_event_queue.append(func)
    return func


@atexit.register
def exit_handler():
    exc_type, exc_value, exc_tb = sys.exc_info()
    [invoke() for invoke in exit_event_queue]
    if exc_value is not None:
        traceback.print_exception(exc_type, exc_value, exc_tb)
