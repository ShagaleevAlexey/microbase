import enum
from http import HTTPStatus

from . import helpers

from sanic.response import json


class MiddlewareType(enum.Enum):
    request = 'request'
    response = 'response'


def _make_response_json(code: int = 200, message: str = None, data: dict = None):
    if data is not None:
        return json(data)

    if message is None:
        message = HTTPStatus(code).phrase

    return json(dict(code=code, message=str(message)), code)


def check_auth(func):

    async def handler(self, request, *args, **kwargs):
        jwt_token = request.headers.get('authorization', None)

        try:
            if jwt_token is None:
                return _make_response_json(401)

            payload = helpers.jwt_payload(jwt_token)
            user_id = payload['uid']
            exp = payload['exp']

            params = {
                'auth': {
                    'access_token': jwt_token,
                    'user_id': user_id,
                    'exp': exp
                }
            }

            request.match_info.update(params)

            if 'application/json' in request.content_type:
                if request.json is not None:
                    request.json.update(params)
        except helpers.ExpiredSignatureError as e:
            return _make_response_json(401)
        except helpers.ExpiredSignatureError as e:
            return _make_response_json(500)
        except Exception as e:
            return _make_response_json(500)

        return await func(self, request, *args, **kwargs)

    return handler
