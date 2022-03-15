"""
@File      : plugin/Paper.py
@Author    : Skeleton_321
@CreateDate: 2022/2/23 17:23
by IntelliJ IDEA
"""
from plugin.PaperMC import PaperMCApiPlugin


class Paper(PaperMCApiPlugin):
    @staticmethod
    def name() -> str:
        return "Paper"

    @staticmethod
    def get_project_name() -> str:
        return "paper"
