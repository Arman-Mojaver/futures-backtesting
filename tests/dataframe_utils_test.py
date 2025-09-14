import pandas as pd
from pandas import Timestamp

from src.dataframe_utils import from_databento_df_to_items

data = {
    "rtype": {
        Timestamp("2024-01-01 23:00:00+0000", tz="UTC"): 33,
        Timestamp("2024-01-01 23:01:00+0000", tz="UTC"): 33,
    },
    "publisher_id": {
        Timestamp("2024-01-01 23:00:00+0000", tz="UTC"): 1,
        Timestamp("2024-01-01 23:01:00+0000", tz="UTC"): 1,
    },
    "instrument_id": {
        Timestamp("2024-01-01 23:00:00+0000", tz="UTC"): 17077,
        Timestamp("2024-01-01 23:01:00+0000", tz="UTC"): 17077,
    },
    "open": {
        Timestamp("2024-01-01 23:00:00+0000", tz="UTC"): 4818.0,
        Timestamp("2024-01-01 23:01:00+0000", tz="UTC"): 4818.75,
    },
    "high": {
        Timestamp("2024-01-01 23:00:00+0000", tz="UTC"): 4819.5,
        Timestamp("2024-01-01 23:01:00+0000", tz="UTC"): 4819.75,
    },
    "low": {
        Timestamp("2024-01-01 23:00:00+0000", tz="UTC"): 4815.75,
        Timestamp("2024-01-01 23:01:00+0000", tz="UTC"): 4818.0,
    },
    "close": {
        Timestamp("2024-01-01 23:00:00+0000", tz="UTC"): 4818.75,
        Timestamp("2024-01-01 23:01:00+0000", tz="UTC"): 4819.75,
    },
    "volume": {
        Timestamp("2024-01-01 23:00:00+0000", tz="UTC"): 1483,
        Timestamp("2024-01-01 23:01:00+0000", tz="UTC"): 783,
    },
    "symbol": {
        Timestamp("2024-01-01 23:00:00+0000", tz="UTC"): "ES.v.0",
        Timestamp("2024-01-01 23:01:00+0000", tz="UTC"): "ES.v.0",
    },
}


def test_from_databento_df_to_items():
    expected_result = [
        {
            "close": 4818.75,
            "high": 4819.5,
            "instrument_id": 17077,
            "low": 4815.75,
            "open": 4818.0,
            "publisher_id": 1,
            "rtype": 33,
            "symbol": "ES.v.0",
            "timestamp": "2024-01-01 23:00:00+00:00",
            "volume": 1483,
        },
        {
            "close": 4819.75,
            "high": 4819.75,
            "instrument_id": 17077,
            "low": 4818.0,
            "open": 4818.75,
            "publisher_id": 1,
            "rtype": 33,
            "symbol": "ES.v.0",
            "timestamp": "2024-01-01 23:01:00+00:00",
            "volume": 783,
        },
    ]

    assert from_databento_df_to_items(pd.DataFrame.from_dict(data)) == expected_result
