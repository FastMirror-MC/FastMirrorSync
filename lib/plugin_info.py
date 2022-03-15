"""
@File      : lib/plugin_info.py
@Author    : Skeleton_321
@CreateDate: 2022/2/22 11:31
by IntelliJ IDEA
"""
import uuid


class Info:
    def name(self) -> str:
        pass

    def client_name(self) -> str:
        return self.name()

    def __client_id__(self):
        return str(uuid.uuid5(uuid.NAMESPACE_X500, self.client_name()))
