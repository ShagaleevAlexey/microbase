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

