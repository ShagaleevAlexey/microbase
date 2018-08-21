import  abc

from .context import Context

from sanic.request import Request
from sanic.response import BaseHTTPResponse, text, json

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
        return json(dict(code=code, message=message), code)

    @abc.abstractmethod
    async def handle(self, request: Request, *args, **kwargs) -> BaseHTTPResponse:
        raise NotImplementedError

class HealthEndpoint(Endpoint):
    """
    Класс endpoint'а для проверки жизненых показателей сервиса
    """
    async def handle(self, request: Request, *args, **kwargs):
        return text("Ok")