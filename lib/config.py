"""
@File      : lib/config.py
@Author    : Skeleton_321
@CreateDate: 2022/2/22 9:06
by IntelliJ IDEA
"""
__all__ = ["get_token", "get_submit_url"]

import os.path

from lib import log

token = ""
submit_url = os.getenv("SUBMIT_URL")


def get_token():
    return token


def get_submit_url():
    return submit_url


if not token:
    if os.path.exists("./auth/token"):
        with open("./auth/token", "r", encoding="utf-8") as fp:
            lines = fp.readlines()
            token = "".join(lines if len(lines) < 2 else lines[1:-1]).strip()
if submit_url == "" or submit_url is None:
    log.error("environment variable SUBMIT_URL is required.")
    log.error("example: https://localhost/submit")
    exit(1)
