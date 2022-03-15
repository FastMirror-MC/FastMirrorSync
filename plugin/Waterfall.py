"""
@File      : plugin/Waterfall.py
@Author    : Skeleton_321
@CreateDate: 2022/3/14 21:16
by IntelliJ IDEA
"""
from plugin.PaperMC import PaperMCApiPlugin


class Waterfall(PaperMCApiPlugin):
    @staticmethod
    def name() -> str:
        return "Waterfall"

    @staticmethod
    def get_project_name() -> str:
        return "waterfall"
