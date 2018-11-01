import abc

from . import helpers
from .context import Context

from sanic.request import Request
from sanic.response import BaseHTTPResponse, text, json, file

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

    def _make_response_json(self, code: int = 200, message: str = None, data: dict = None):
        if data is not None:
            return json(data)

        if message is None:
            message = HTTPStatus(code).phrase

        return json(dict(code=code, message=str(message)), code)

    async def _make_response_file(self, filepath: str):
        return await file(filepath)

    @abc.abstractmethod
    async def handle(self, request: Request, *args, **kwargs) -> BaseHTTPResponse:
        raise NotImplementedError


class BasicEndpoint(Endpoint):

    def params_from_dictparams(self, params: dict):
        args = {}

        for key in params:
            value = params[key]

            if isinstance(value, list) and len(value) == 1:
                value = value[0]

            args[key] = value

        return args

    async def handle(self, request: Request, auth: dict, *args, **kwargs) -> BaseHTTPResponse:
        body = {}

        if request.match_info is not None:
            body = dict(request.match_info)

        if 'application/json' in request.content_type and request.json is not None:
            body.update(request.json)

        if request.method == 'GET' and request.args is not None and len(request.args) > 0:
            args = self.params_from_dictparams(request.args)

            body.update(args)

        if request.files is not None and len(request.files) > 0:
            body.update(request.files)

        if request.form is not None and len(request.form) > 0:
            args = request.form

            if 'multipart/form-data' in request.content_type:
                args = self.params_from_dictparams(args)

            body.update(args)


        if auth is not None:
            body['auth'] = auth

        if request.method == 'GET':
            return await self._method_get(request=request, body=body)
        elif request.method == 'POST':
            return await self._method_post(request=request, body=body)
        elif request.method == 'DELETE':
            return await self._method_delete(request=request, body=body)
        elif request.method == 'PUT':
            return await self._method_put(request=request, body=body)

        return self._make_response_json(code=405, message='Method Not Allowed')

    async def _method_get(self, request: Request, *, body: dict):
        return self._make_response_json(code=500, message='GET Not Impl')

    async def _method_post(self, request: Request, *, body: dict):
        return self._make_response_json(code=500, message='POST Not Impl')

    async def _method_delete(self, request: Request, *, body: dict):
        return self._make_response_json(code=500, message='DELETE Not Impl')

    async def _method_put(self, request: Request, *, body: dict):
        return self._make_response_json(code=500, message='PUT Not Impl')


class AuthEndpoint(BasicEndpoint):
    """
    Класс endpoint'а для проверки авторизации запроса
    """
    async def handle(self, request: Request, *args, **kwargs) -> BaseHTTPResponse:
        params: dict
        jwt_token = request.headers.get('authorization', None)

        try:
            if jwt_token is None or not jwt_token:  # add behavior when empty jwt_token reach
                return self._make_response_json(401)

            payload = helpers.jwt_payload(jwt_token)
            user_id = payload['uid']
            exp = payload['exp']
            user_type = payload['type']

            params = {
                'access_token': jwt_token,
                'user_id': user_id,
                'exp': exp,
                'user_type': user_type
            }
        except helpers.ExpiredSignatureError as e:
            return self._make_response_json(401)
        except helpers.InvalidSignatureError as e:
            return self._make_response_json(401)
        except helpers.InvalidSignatureError as e:
            return self._make_response_json(401)
        except helpers.InvalidTokenError as e:
            return self._make_response_json(401)
        except helpers.DecodeError as e:
            return self._make_response_json(401)
        except Exception as e:
            return self._make_response_json(500)

        return await super(AuthEndpoint, self).handle(request, params, args, kwargs)


class HealthEndpoint(Endpoint):
    """
    Класс endpoint'а для проверки жизненых показателей сервиса
    """
    async def handle(self, request: Request, *args, **kwargs):
        return text("Ok")
