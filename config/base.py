from __future__ import annotations


class BaseConfig:
    ENVIRONMENT: str | None = None

    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"

    def is_development(self) -> bool:
        return self.ENVIRONMENT == "development"

    def is_testing(self) -> bool:
        return self.ENVIRONMENT == "testing"

    def __repr__(self) -> str:
        return self.__class__.__name__
