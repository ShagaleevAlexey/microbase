import abc
from http import HTTPStatus
import json

from . import helpers
from .context import Context

from microbase_auth import AuthManager
from microbase_auth.auth import DecodeError, ExpiredSignatureError, InvalidSignatureError, InvalidTokenError

from sanic.request import Request
from sanic.response import BaseHTTPResponse, text, json, file

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

    def _make_response_json(self, code: int = 200, message: str = None, data: dict = None, error_code: int = None) -> BaseHTTPResponse:
        if data is not None:
            return json(data)

        if message is None:
            message = HTTPStatus(code).phrase

        if error_code is None:
            error_code = code

        data = {
            'code': error_code,
            'message': message
        }

        return json(data, status=code)

    async def _make_response_file(self, filepath: str) -> BaseHTTPResponse:
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
            files = {}

            for key in request.files:
                if isinstance(request.files[key], list):
                    files[key] = [{'type': file.type, 'body': file.body, 'name': file.name} for file in request.files[key]]
                else:
                    files[key] = request.files

            body.update(files)

        if request.form is not None and len(request.form) > 0:
            args = request.form

            if 'multipart/form-data' in request.content_type:
                args = self.params_from_dictparams(args)

            body.update(args)

        if auth is not None:
            body['auth'] = auth

        for header in request.headers:
            if header[:2].lower() == 'x-':
                body[header] = request.headers[header]

        return await self._method(request, body, *args, **kwargs)

    async def _method(self, request: Request, body: dict, *args, **kwargs) -> BaseHTTPResponse:
        if request.method == 'GET':
            return await self._method_get(request, body, *args, **kwargs)
        elif request.method == 'POST':
            return await self._method_post(request, body, *args, **kwargs)
        elif request.method == 'DELETE':
            return await self._method_delete(request, body, *args, **kwargs)
        elif request.method == 'PUT':
            return await self._method_put(request, body, *args, **kwargs)

        return self._make_response_json(code=405, message='Method Not Allowed')

    async def _method_get(self, request: Request, body: dict, *args, **kwargs) -> BaseHTTPResponse:
        return self._make_response_json(code=500, message='GET Not Impl')

    async def _method_post(self, request: Request, body: dict, *args, **kwargs) -> BaseHTTPResponse:
        return self._make_response_json(code=500, message='POST Not Impl')

    async def _method_delete(self, request: Request, body: dict, *args, **kwargs) -> BaseHTTPResponse:
        return self._make_response_json(code=500, message='DELETE Not Impl')

    async def _method_put(self, request: Request, body: dict, *args, **kwargs) -> BaseHTTPResponse:
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

            auth: AuthManager = self.context.auth
            params, _ = auth.get_any_payload(jwt_token)
        except ExpiredSignatureError as e:
            return self._make_response_json(401)
        except InvalidSignatureError as e:
            return self._make_response_json(401)
        except InvalidSignatureError as e:
            return self._make_response_json(401)
        except InvalidTokenError as e:
            return self._make_response_json(401)
        except DecodeError as e:
            return self._make_response_json(401)
        except Exception as e:
            return self._make_response_json(500)

        return await super(AuthEndpoint, self).handle(request, params, args, kwargs)


class HealthEndpoint(Endpoint):
    """
    Класс endpoint'а для проверки жизненых показателей сервиса
    """
    async def handle(self, request: Request, *args, **kwargs) -> BaseHTTPResponse:
        return text("Ok")
