from __future__ import annotations

import os


class BaseConfig:
    ENVIRONMENT: str | None = None
    DATABENTO_API_KEY: str = os.getenv("DATABENTO_API_KEY", "")

    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"

    def is_development(self) -> bool:
        return self.ENVIRONMENT == "development"

    def is_testing(self) -> bool:
        return self.ENVIRONMENT == "testing"

    def price_data_path(self) -> str:
        return f"price_data/{self.ENVIRONMENT}"

    def __repr__(self) -> str:
        return self.__class__.__name__
