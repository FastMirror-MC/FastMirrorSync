"""
@File      : lib/plugin.py
@Author    : Skeleton_321
@CreateDate: 2022/2/22 11:32
by IntelliJ IDEA
"""
import uuid

from lib import log
from lib.http import aio_download
from lib.log import logger
from lib.utils import get_mills_time
from lib.version import string_version, integer_version


__all__ = ["Plugin", "GithubApiPlugin", "JenkinsApiPlugin"]


def run_all(o, fn, *args, cls: type = None, queue: set = None, **kwargs):
    queue = queue if queue is not None else set()
    cls = cls if cls is not None else o.__class__

    if cls == object or cls == type(object):
        return
    for clazz in cls.__bases__:
        if clazz == object or clazz in queue:
            continue
        run_all(o, fn, *args, cls=clazz, queue=queue, **kwargs)
        if not getattr(clazz, "__disable_auto_init__", False):
            # (clazz.__init__ if fn == "__init__" else getattr(clazz, fn, lambda *a, **kw: None))(o, *args, **kwargs)
            getattr(clazz, fn, lambda *a, **kw: None)(o, *args, **kwargs)
            queue.add(clazz)
            log.info(queue)


async def async_run_all(o, fn, *args, cls: type = None, queue: set = None, **kwargs):
    queue = queue if queue is not None else set()
    cls = cls if cls is not None else o.__class__

    if cls == object or cls == type(object):
        return
    for clazz in cls.__bases__:
        if clazz == object or clazz in queue:
            continue
        await async_run_all(o, fn, *args, cls=clazz, queue=queue, **kwargs)
        if not getattr(clazz, "__disable_auto_init__", False) and hasattr(clazz, fn):
            await getattr(clazz, fn)(o, *args, **kwargs)
            queue.add(clazz)


class Plugin:
    def __init__(self):
        installed = getattr(self, "__installed_modules__", set())
        log.debug(f"{self.name()} has installed: {installed}")
        if "logger" not in installed:
            self.debug = log.debug
            self.info = log.info
            self.warning = log.warning
            self.error = log.error
            self.exception = log.exception
            self.critical = log.critical
        pass

    @staticmethod
    def name() -> str:
        pass

    def client_name(self) -> str:
        return self.name()

    def client_id(self):
        return str(uuid.uuid5(uuid.NAMESPACE_X500, self.client_name()))

    def __enter__(self):
        self.__start_time__ = get_mills_time()
        self.info(f"task {self.name()} start.")
        return self

    async def __aenter__(self):
        self.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.info(f"task {self.name()} finished in {(get_mills_time() - self.__start_time__) / 1000}s.")
        if exc_type is not None:
            self.exception("exit with exception.", exc_info=exc_type)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.__exit__(exc_type, exc_val, exc_tb)

    async def run(self) -> None:
        pass


@logger
@aio_download
@string_version("./config")
class GithubApiPlugin(Plugin):
    __disable_auto_init__ = True

    def get_version(self, json) -> str:
        pass

    def get_core_version(self, json) -> str:
        return f"build{self.get_build_number(json)}"

    def get_build_number(self, json) -> int:
        pass

    @staticmethod
    def get_asset(json) -> dict:
        pass

    @staticmethod
    def get_api_url() -> str:
        pass

    async def run(self) -> None:
        for publish in await self.get(self.get_api_url()):
            version = self.get_version(publish)
            core_version = self.get_core_version(publish)
            build = self.get_build_number(publish)
            asset = self.get_asset(publish)
            release = not publish["prerelease"]
            update_time = publish["published_at"]

            if not self.need_update(version, core_version):
                continue

            if asset is None:
                continue

            self.info(f"{version} find a newer version: {core_version}")
            await self.submit(
                url=asset["browser_download_url"],
                version=version,
                core_version=core_version,
                build=build,
                update_time=update_time,
                release=release
            )
            self.write(version, core_version)


@logger
@aio_download
@integer_version("./config")
class JenkinsApiPlugin(Plugin):
    __disable_auto_init__ = True

    def get_version(self, json) -> str:
        pass

    @staticmethod
    def get_is_release(json) -> bool:
        return True

    @staticmethod
    def get_asset(json) -> dict:
        pass

    @staticmethod
    def get_ci_url() -> str:
        pass

    async def run(self) -> None:
        json = await self.get(f"{self.get_ci_url()}/lastSuccessfulBuild/api/json")
        build = json["number"]
        version = self.get_version(json)
        release = self.get_is_release(json)

        while True:
            if len(json["artifacts"]) < 1:
                self.warning(f"this build(#{build}) has no artifact. skipped. ")
                break
            if json["result"] != "SUCCESS":
                break
            if not self.need_update(version, build):
                break

            asset = self.get_asset(json)
            self.info(f"{version} find a new build {build}")
            await self.submit(
                url=f'{json["url"]}artifact/{asset["relativePath"]}',
                version=version,
                build=build,
                release=release,
                update_time=json["timestamp"] // 1000
            )
            break
        self.write(version, build)
        self.info(f"{version} is up-to-date.")
