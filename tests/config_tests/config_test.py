import os

import pytest

from config import get_config
from testing_utils.environment_utils import temporary_disable_os_environ_is_test


def test_default_test_environment_is_test():
    from config import config  # noqa: PLC0415

    assert config.is_testing()


def test_undefined_os_environ_returns_development():
    with temporary_disable_os_environ_is_test():
        config = get_config()
        assert config.is_development()


def test_environment_is_production_from_os_environ():
    with temporary_disable_os_environ_is_test():
        os.environ["ENVIRONMENT"] = "production"
        config = get_config()
        assert config.is_production()


def test_environment_is_development_from_os_environ():
    with temporary_disable_os_environ_is_test():
        os.environ["ENVIRONMENT"] = "development"
        config = get_config()
        assert config.is_development()


def test_environment_is_test_from_os_environ():
    with temporary_disable_os_environ_is_test():
        os.environ["ENVIRONMENT"] = "testing"
        config = get_config()
        assert config.is_testing()


def test_invalid_environment_from_os_environ_returns_error():
    with temporary_disable_os_environ_is_test():
        os.environ["ENVIRONMENT"] = "invalid_environment_name"
        with pytest.raises(ValueError):
            get_config()


@pytest.mark.parametrize(
    ("environment", "expected_string"),
    [
        ("production", "ProductionConfig"),
        ("development", "DevelopmentConfig"),
        ("testing", "TestingConfig"),
    ],
)
def test_base_config_repr(environment, expected_string):
    with temporary_disable_os_environ_is_test():
        os.environ["ENVIRONMENT"] = environment
        config = get_config()

        assert repr(config) == expected_string
