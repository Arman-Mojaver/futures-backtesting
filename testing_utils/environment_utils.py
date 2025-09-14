import os
from collections.abc import Generator
from contextlib import contextmanager


@contextmanager
def temporary_disable_os_environ_is_test() -> Generator[None]:
    if os.environ.get("ENVIRONMENT"):
        del os.environ["ENVIRONMENT"]

    yield

    os.environ["ENVIRONMENT"] = "testing"
