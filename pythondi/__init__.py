import inspect
from functools import wraps

_PROVIDER = None


class Provider:
    def __init__(self):
        self._bindings = {}

    def bind(self, cls, new_cls) -> None:
        """Binding class to another class"""
        self._bindings[cls] = new_cls

    @property
    def bindings(self) -> dict:
        """Return current binding classes"""
        return self._bindings


def configure(provider: Provider) -> None:
    """Configure provider"""
    global _PROVIDER

    if _PROVIDER:
        raise Exception('Already injected')

    _PROVIDER = provider


def configure_after_clear(provider: Provider) -> None:
    """Clear existing provider and configure new provider"""
    global _PROVIDER

    _PROVIDER = provider


def inject(**params):
    def inner_func(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Case of auto injection
            if params == {}:
                annotations = inspect.getfullargspec(func).annotations
                for k, v in annotations.items():
                    if v in _PROVIDER.bindings:
                        kwargs[k] = _PROVIDER.bindings[v]()
            # Case of manual injection
            else:
                for k, v in params.items():
                    kwargs[k] = v()
            func(*args, **kwargs)
        return wrapper
    return inner_func
