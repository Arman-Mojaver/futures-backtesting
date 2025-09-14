import pytest

from src.databento_client import DatabentoClient


def test_init_with_empty_api_key_raises_value_error():
    with pytest.raises(ValueError):
        DatabentoClient(api_key="")
