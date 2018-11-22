import inspect
from asyncio import BaseEventLoop
from enum import Enum
from typing import Callable

from sanic import Sanic

from microbase import Application
from microbase.context import Context, context


class HookNames(Enum):
    before_server_start = 'before_server_start'
    after_server_start = 'after_server_start'
    before_server_stop = 'before_server_stop'
    after_server_stop = 'after_server_stop'


class HookHandler(object):

    def __init__(self, app: Application, handler: Callable[[Application, Context, BaseEventLoop], None]):
        super().__init__()
        self._app = app
        self._handler = handler

    async def __call__(self, _: Sanic, loop: BaseEventLoop):
        if inspect.iscoroutinefunction(self._handler):
            await self._handler(self._app, context, loop)
        else:
            self._handler(self._app, self._app.context, loop)
