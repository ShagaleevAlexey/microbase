from typing import Iterable

from microbase.exception import RouteError
from microbase.endpoint import Endpoint


class Route(object):
    """
    Базовый класс для реализации маршрута
    """
    def __init__(self, handler: Endpoint, uri: str, methods: Iterable = frozenset({'GET'}),
                 strict_slashes: bool = False, name: str = None):
        super(Route, self).__init__()

        if not isinstance(handler, Endpoint):
            raise RouteError('Handler must be instance of Endpoint class')

        self._handler = handler
        self._uri = uri
        self._methods = methods
        self._strict_slashes = strict_slashes

        self._name = name
        if self._name is None:
            self._name = self._handler.__name__

    @property
    def handler(self) -> Endpoint:
        return self._handler

    @property
    def uri(self) -> str:
        return self._uri

    @property
    def methods(self) -> Iterable:
        return self._methods

    @property
    def strict_slashes(self) -> bool:
        return self._strict_slashes

    @property
    def name(self):
        return self._name
