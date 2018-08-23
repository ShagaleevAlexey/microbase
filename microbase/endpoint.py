import  abc

from .context import Context

from sanic.request import Request
from sanic.response import BaseHTTPResponse, text, json

from http import HTTPStatus

# from .context import Context

class Endpoint(object, metaclass=abc.ABCMeta):
    """
    Базовый класс для реализации endpoint'а
    """
    context: Context

    def __init__(self, context: Context):
        self.context = context
        self.__name__ = self.__class__.__name__

    async def __call__(self, request: Request, *args, **kwargs):
        return await self.handle(request, *args, kwargs)

    def _make_response_json(self, code: int = 200, message: str = ''):
        if isinstance(message, str) and len(message) == 0:
            message = HTTPStatus(code).phrase

        return json(dict(code=code, message=str(message)), code)

    @abc.abstractmethod
    async def handle(self, request: Request, *args, **kwargs) -> BaseHTTPResponse:
        raise NotImplementedError

class HealthEndpoint(Endpoint):
    """
    Класс endpoint'а для проверки жизненых показателей сервиса
    """
    async def handle(self, request: Request, *args, **kwargs):
        return text("Ok")