# def salty_password(original_password: str, salt: str = None) -> (str, str):
#     import sha3
#
#     keccack256 = sha3.keccak_256()
#
#     if salt is None:
#         import secrets
#         salt = secrets.token_hex(16)
#
#     keccack256.update(str.encode(original_password + salt))
#
#     return (keccack256.hexdigest(), salt)

import jwt
from jwt import ExpiredSignatureError

__JWT_SECRET = '65zkFWQV'


def jwt_token(payload: dict, algo: str = 'HS256') -> str:
    token = jwt.encode(payload, __JWT_SECRET, algo).decode('utf-8')

    return token


def jwt_payload(token: str, algo: str = 'HS256') -> dict:
    payload = jwt.decode(token, __JWT_SECRET, algorithms=[algo])

    return payload
