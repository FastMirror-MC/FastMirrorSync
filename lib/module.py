"""
@File      : lib/module.py
@Author    : Skeleton_321
@CreateDate: 2022/2/22 21:52
by IntelliJ IDEA
"""
from lib import log


def mount(cls, func, name=None):
    name = name if name is not None else func.__name__
    if not hasattr(cls, name):
        setattr(cls, name, func)


def override(cls, func, name=None):
    name = name if name is not None else func.__name__
    if hasattr(cls, name):
        setattr(cls, f"__origin_{name}", getattr(cls, name))
    setattr(cls, name, func)


def injection(cls, func, name=None):
    name = name if name is not None else func.__name__
    inject_list_name = f"__injected_{name}"
    if hasattr(cls, inject_list_name):
        injected_list = getattr(cls, inject_list_name)
        injected_list.add(func)
    else:
        origin_function = getattr(cls, name)

        setattr(cls, inject_list_name, set())
        injected_list = getattr(cls, inject_list_name)
        injected_list.add(func)

        if origin_function:
            def injector(self, *args, **kwargs):
                for f in injected_list:
                    f(self, *args, **kwargs)
                return origin_function(self, *args, **kwargs)
        else:
            def injector(self, *args, **kwargs):
                for f in injected_list:
                    f(self, *args, **kwargs)

        setattr(cls, name, injector)


def register(module_name):
    def call(func):
        def decorator(cls, *args, **kwargs):
            if not hasattr(cls, "__installed_modules__"):
                setattr(cls, "__installed_modules__", set())

            if module_name not in cls.__installed_modules__:
                cls.__installed_modules__.add(module_name)
                func(cls, *args, **kwargs)
            else:
                log.warning(f"module {module_name} has installed.")
            return cls

        return decorator
    return call
