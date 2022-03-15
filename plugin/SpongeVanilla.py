"""
@File      : plugin/SpongeVanilla.py
@Author    : Skeleton_321
@CreateDate: 2022/3/14 21:12
by IntelliJ IDEA
"""
from .Sponge import SpongeApiPlugin


class SpongeVanilla(SpongeApiPlugin):
    @staticmethod
    def name() -> str:
        return "SpongeVanilla"

    @staticmethod
    def get_project_name():
        return "spongevanilla"
