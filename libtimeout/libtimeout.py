import signal

from .exceptions import TimeoutException


def timeout_handler(signum: int, frame):
    raise TimeoutException("Timeout occoured")


class Timeout:
    def __init__(self, timeout_limit: int = 10, retry_limit: int = 0, **kwargs) -> None:
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
