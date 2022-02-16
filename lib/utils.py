"""
@File      : src/client/utils.py
@Author    : Skeleton_321
@CreateDate: 2022/2/5 21:52
by IntelliJ IDEA
"""
import datetime
import hashlib
import time

import pytz
import requests

get = requests.get
post = requests.post
USERAGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 " \
            "Safari/537.36 Edg/97.0.1072.76"


def proxy_invoke(log, callback, sign, retry=1, **kwargs):
    log.debug(f"{sign}: {kwargs['url']}")
    for i in range(retry):
        res = callback(**kwargs)
        if 200 <= res.status_code < 300:
            if callback != post:
                kwargs["proxies"] = {"http": "localhost:10809"}
            log.debug("request success.")
            return res
        log.warning(f"{sign} failed(status code={res.status_code}). retry({i + 1}/{retry})")
        log.warning(res.text)
    log.error(f"{sign} request failed.")
    return None


def get_mills_time():
    return int(time.time() * 1000)


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


def if_file_invalid(log, stream, checksum: str, mode: str):
    if checksum is None:
        log.warning("need origin checksum. skipped.")
        return False
    return checksum.lower() != get_checksum(stream, mode)


def dt2str(dt: datetime.datetime):
    return dt.astimezone(pytz.UTC).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


class UptoDateException(Exception):
    pass


datetime.timedelta(seconds=12)
