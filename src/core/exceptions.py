from typing import Any


class AppException(Exception):
    pass


class ObjectAlreadyExists(AppException):
    pass


class ObjectNotExists(AppException):
    pass
