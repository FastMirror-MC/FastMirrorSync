"""
@File      : lib/utils.py
@Author    : Skeleton_321
@CreateDate: 2022/2/22 8:39
by IntelliJ IDEA
"""
from __future__ import annotations

import datetime
import hashlib
import time

import pytz

from lib import log

__all__ = ["datetime2str", "get_checksum", "if_file_invalid", "get_mills_time"]
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
