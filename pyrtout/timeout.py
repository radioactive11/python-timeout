import signal
from functools import wraps

from .exceptions import TimeoutException


def timeout_handler(signum: int, frame):
    raise TimeoutException("Timeout occoured")


class Timeout:
    def __init__(self, timeout_limit: int = 10, retry_limit: int = 0, **kwargs) -> None:
        """Retry a function until it succeeds or the timeout limit is reached.

        Args:
            timeout_limit (int, optional): Timeout limit in seconds. Defaults to 10.
            retry_limit (int, optional): Number of retry attempts. Defaults to 0.
            timeout_exception (Exception, optional): Exception to raise on timeout. Defaults to TimeoutException.
            timeout_handler (callable, optional): Handler to call on timeout. Must raise timeout_exception. Defaults to timeout_handler.

        Raises:
            TypeError: Default Timeout Exception.
        """
        self.__timeout_limit: int = timeout_limit
        self.__retry_limit: int = retry_limit
        self.__timeout_exception = kwargs.get("timeout_exception", TimeoutException)
        self.__timeout_handler: callable = kwargs.get(
            "timeout_handler", self.__timeout_handler
        )

        if not issubclass(self.__timeout_exception, Exception):
            raise TypeError("timeout_exception must be a subclass of Exception")

    def __timeout_handler(self, signum: int, frame):
        raise self.__timeout_exception("Timeout occoured")

    def bind(self, **kwargs):
        def timeout_decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                nonlocal self

                signal.signal(signal.SIGALRM, self.__timeout_handler)
                signal.alarm(self.__timeout_limit)

                retry: int = 0

                while retry <= self.__retry_limit:
                    try:
                        return func(*args, **kwargs)

                    except self.__timeout_exception:
                        retry += 1
                        signal.alarm(self.__timeout_limit)

            signal.alarm(0)
            return wrapper

        return timeout_decorator
