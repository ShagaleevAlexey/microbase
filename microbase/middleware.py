import enum


class MiddlewareType(enum.Enum):
    request = 'request'
    response = 'response'