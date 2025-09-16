from __future__ import annotations

from typing import TYPE_CHECKING

import pandas as pd
from nautilus_trader.common.enums import LogColor
from nautilus_trader.config import PositiveInt, StrategyConfig
from nautilus_trader.core.correctness import PyCondition
from nautilus_trader.indicators import SimpleMovingAverage
from nautilus_trader.model import (
    Bar,
    BarType,
    InstrumentId,
    OrderBook,
    OrderBookDeltas,
    Quantity,
    QuoteTick,
    TradeTick,
)
from nautilus_trader.model.enums import OrderSide, TimeInForce
from nautilus_trader.trading import Strategy

if TYPE_CHECKING:
    from decimal import Decimal

    from nautilus_trader.core.data import Data
    from nautilus_trader.core.message import Event
    from nautilus_trader.model.instruments import Instrument
    from nautilus_trader.model.orders import MarketOrder


class MACrossConfig(StrategyConfig, frozen=True):
    instrument_id: InstrumentId
    bar_type: BarType
    trade_size: Decimal
    fast_ma_period: PositiveInt = 10
    slow_ma_period: PositiveInt = 20
    request_bars: bool = True
    order_quantity_precision: int | None = None
    order_time_in_force: TimeInForce | None = None
    close_positions_on_stop: bool = True
    reduce_only_on_stop: bool = True


class MACross(Strategy):
    def __init__(self, config: MACrossConfig) -> None:
        PyCondition.is_true(
            config.fast_ma_period < config.slow_ma_period,
            "{config.fast_ma_period=} must be less than {config.slow_ma_period=}",
        )
        super().__init__(config)

        self.instrument: Instrument = None

        self.fast_ma = SimpleMovingAverage(config.fast_ma_period)
        self.slow_ma = SimpleMovingAverage(config.slow_ma_period)

    def on_start(self) -> None:
        self.instrument = self.cache.instrument(self.config.instrument_id)
        if self.instrument is None:
            self.log.error(f"Could not find instrument for {self.config.instrument_id}")  # noqa: G004
            self.stop()
            return

        self.register_indicator_for_bars(self.config.bar_type, self.fast_ma)
        self.register_indicator_for_bars(self.config.bar_type, self.slow_ma)

        if self.config.request_bars:
            self.request_bars(
                self.config.bar_type,
                start=self._clock.utc_now() - pd.Timedelta(days=1),
            )

        self.subscribe_bars(self.config.bar_type)

    def on_instrument(self, instrument: Instrument) -> None:
        pass

    def on_order_book_deltas(self, deltas: OrderBookDeltas) -> None:
        pass

    def on_order_book(self, order_book: OrderBook) -> None:
        pass

    def on_quote_tick(self, tick: QuoteTick) -> None:
        self.log.info(repr(tick), LogColor.CYAN)

    def on_trade_tick(self, tick: TradeTick) -> None:
        self.log.info(repr(tick), LogColor.CYAN)

    def on_bar(self, bar: Bar) -> None:
        self.log.info(repr(bar), LogColor.CYAN)

        if not self.indicators_initialized():
            self.log.info(
                "Waiting for indicators to warm up "  # noqa: G004
                f"[{self.cache.bar_count(self.config.bar_type)}]",
                color=LogColor.BLUE,
            )
            return

        if bar.is_single_price():
            self._log.warning("Bar OHLC is single price; implies no market information")
            return

        # BUY LOGIC
        if self.fast_ma.value >= self.slow_ma.value:
            if self.portfolio.is_flat(self.config.instrument_id):
                self.buy()
            elif self.portfolio.is_net_short(self.config.instrument_id):
                self.close_all_positions(self.config.instrument_id)
                self.buy()
        # SELL LOGIC
        elif self.fast_ma.value < self.slow_ma.value:
            if self.portfolio.is_flat(self.config.instrument_id):
                self.sell()
            elif self.portfolio.is_net_long(self.config.instrument_id):
                self.close_all_positions(self.config.instrument_id)
                self.sell()

    def buy(self) -> None:
        order: MarketOrder = self.order_factory.market(
            instrument_id=self.config.instrument_id,
            order_side=OrderSide.BUY,
            quantity=self.create_order_qty(),
            time_in_force=self.config.order_time_in_force or TimeInForce.GTC,
        )

        self.submit_order(order)

    def sell(self) -> None:
        order: MarketOrder = self.order_factory.market(
            instrument_id=self.config.instrument_id,
            order_side=OrderSide.SELL,
            quantity=self.create_order_qty(),
            time_in_force=self.config.order_time_in_force or TimeInForce.GTC,
        )

        self.submit_order(order)

    def create_order_qty(self) -> Quantity:
        if self.config.order_quantity_precision is not None:
            return Quantity(self.config.trade_size, self.config.order_quantity_precision)

        return self.instrument.make_qty(self.config.trade_size)

    def on_data(self, data: Data) -> None:
        pass

    def on_event(self, event: Event) -> None:
        pass

    def on_stop(self) -> None:
        self.cancel_all_orders(self.config.instrument_id)
        if self.config.close_positions_on_stop:
            self.close_all_positions(
                instrument_id=self.config.instrument_id,
                reduce_only=self.config.reduce_only_on_stop,
            )

    def on_reset(self) -> None:
        self.fast_ma.reset()
        self.slow_ma.reset()

    def on_save(self) -> dict[str, bytes]:
        return {}

    def on_load(self, state: dict[str, bytes]) -> None:
        pass

    def on_dispose(self) -> None:
        pass
