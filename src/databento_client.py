import databento
from databento.common.dbnstore import DBNStore


class DatabentoClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self._validate_api_key_exists()
        self.client = databento.Historical(self.api_key)

    def _validate_api_key_exists(self):
        if not self.api_key:
            err = f"Missing Databento API key: {self.api_key}"
            raise ValueError(err)

    def get_range(
        self,
        start_date: str,
        end_date: str,
        limit: int = 1,
    ) -> DBNStore:
        return self.client.timeseries.get_range(
            dataset="GLBX.MDP3",
            schema="ohlcv-1m",
            symbols="ES.v.0",
            stype_in="continuous",
            start=f"{start_date}T00:00:00",
            end=f"{end_date}T00:00:00",
            limit=limit,
        )
