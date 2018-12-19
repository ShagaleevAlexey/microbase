from sanic_envconfig import EnvConfig
from enum import Enum


class LogFormat(Enum):
    json = 'json'
    plain = 'plain'


class BaseConfig(EnvConfig):
    """
    Базовый класс для создания конфигураций
    """
    pass


class GeneralConfig(BaseConfig):
    """
    Основные конфигурации
    """

    DEBUG: bool = False
    LOGO: str   = """
          (_)              | |                   
 _ __ ___  _  ___ _ __ ___ | |__   __ _ ___  ___ 
| '_ ` _ \| |/ __| '__/ _ \| '_ \ / _` / __|/ _ \\
| | | | | | | (__| | | (_) | |_) | (_| \__ \  __/
|_| |_| |_|_|\___|_|  \___/|_.__/ \__,_|___/\___|"""

    APP_HOST: str               = '0.0.0.0'
    APP_PORT: int               = 10080
    APP_TOKEN: str              = ''
    APP_PREFIX: str             = ''

    LOG_FORMAT: LogFormat       = LogFormat.json
    LOG_LEVEL: str              = 'INFO'

    USER_JWT_SIGNATURE: str     = '43pKTQr9'
    SERVICE_JWT_SIGNATURE: str  = 'H6U2XmhM'

    WORKERS: int                = 1
    REQUEST_MAX_SIZE: int       = 20000000
