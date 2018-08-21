from collections import UserDict, Mapping
from typing import Any


class _ContextMutable(UserDict):
    def set(self, key, value):
        self[key] = value

    def __getattr__(self, item):
        if item not in self:
            raise AttributeError(item)
        return self[item]


class Context(Mapping):
    def __init__(self, mutable_context: _ContextMutable):
        super(Context, self).__init__()
        self._context = mutable_context

    def __getitem__(self, key):
        return self._context[key]

    def __iter__(self):
        return self._context.__iter__()

    def __len__(self):
        return len(self._context)

    def __getattr__(self, name: str) -> Any:
        return getattr(self._context, name)


_context_mutable = _ContextMutable()
context = Context(_context_mutable)