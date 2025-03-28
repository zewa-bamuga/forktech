import enum


class ErrorCodes(enum.StrEnum):
    api_error = enum.auto()
    not_found = enum.auto()
    database_error = enum.auto()
