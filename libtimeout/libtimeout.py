import signal

from exceptions import TimeoutException


def timeout_handler(signum: int, frame):
    raise TimeoutException("Timeout occoured")


def timeout(**kwargs):
    timeout_limit: int = kwargs.get("timeout_limit", 10)
    retry_limit: int = kwargs.get("retry_limit", 1)

    def timeout_decorator(func):
        def wrapper(*args, **kwargs):
            nonlocal timeout_limit
            nonlocal retry_limit

            print(f"TIMEOUT_LIMIT: {timeout_limit}")

            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(timeout_limit)

            retry: int = 0

            while retry < retry_limit:
                try:
                    return func(*args, **kwargs)

                except TimeoutException:
                    retry += 1
                    signal.alarm(timeout_limit)

        signal.alarm(0)
        return wrapper

    return timeout_decorator


if __name__ == "__main__":

    @timeout(timeout_limit=2, retry_limit=3)
    def example(*args):
        import time

        ctr = 0
        while ctr < 10:
            print(f"{ctr=}")
            ctr += 1
            time.sleep(1)
