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

    APP_HOST: str               = '0.0.0.0'
    APP_PORT: int               = 10080
    APP_TOKEN: str              = ''
    APP_PREFIX: str             = ''
    DEBUG: bool                 = False
    USER_JWT_SIGNATURE: str     = '65zkFWQV'
    SERVICE_JWT_SIGNATURE: str  = ''
    API_HOST: str               = 'https://google.ru'
    LOG_FORMAT: LogFormat       = LogFormat.json
    LOG_LEVEL: str              = 'INFO'
    WORKERS: int                = 1
    REQUEST_MAX_SIZE: int       = 20000000
