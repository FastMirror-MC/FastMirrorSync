"""
@File      : lib/__init__.py.py
@Author    : Skeleton_321
@CreateDate: 2022/2/22 8:28
by IntelliJ IDEA
"""
import os

__root__ = os.getenv("HOME")
__root__ = __root__ if __root__ else "."
__config_root_path__ = f"{__root__}/config"
__auth_root_path__ = f"{__root__}/auth"
__cache_root_path__ = f"{__root__}/tmp"
__log_root_path__ = f"{__root__}/log"

if not os.path.exists(__config_root_path__):
    os.makedirs(__config_root_path__)
if not os.path.exists(__auth_root_path__):
    os.makedirs(__auth_root_path__)
if not os.path.exists(__cache_root_path__):
    os.makedirs(__cache_root_path__)
if not os.path.exists(__log_root_path__):
    os.makedirs(__log_root_path__)
