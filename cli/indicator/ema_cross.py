from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path

import click
from databento.common.dbnstore import DBNStore
from nautilus_trader.adapters.databento import DatabentoDataLoader
from nautilus_trader.backtest.engine import BacktestEngine
from nautilus_trader.examples.strategies.ema_cross import EMACross, EMACrossConfig
from nautilus_trader.model import (
    Currency,
    InstrumentId,
    Money,
    Price,
    Quantity,
    Symbol,
    Venue,
)
from nautilus_trader.model.currencies import USD
from nautilus_trader.model.enums import AccountType, AssetClass, OmsType
from nautilus_trader.model.instruments import FuturesContract

from config import config
from src.utils import replace_nan_to_none, save_data


@click.option(
    "-f",
    "--fast_period",
    default=20,
    type=int,
    help="Fast EMA period (default: 20)",
)
@click.option(
    "-s",
    "--slow_period",
    default=50,
    type=int,
    help="Slow EMA period (default: 50)",
)
@click.command("ema_cross", help="Backtest EMA cross")
def ema_cross(fast_period: int, slow_period: int) -> None:
    file_path = sorted(Path(config.price_data_path()).glob("*.dbn"))[-1]
    metadata = DBNStore.from_file(file_path).metadata

    symbol_str = metadata.symbols[0]
    symbol = Symbol(symbol_str)
    venue_str = metadata.dataset.split(".")[0]
    venue = Venue(venue_str)

    instrument_id = InstrumentId.from_str(f"{symbol_str}.{venue_str}")
    loader = DatabentoDataLoader()
    data = loader.from_dbn_file(
        path=file_path,
        instrument_id=instrument_id,
    )

    engine = BacktestEngine()
    engine.add_venue(
        venue=venue,
        oms_type=OmsType.NETTING,
        account_type=AccountType.MARGIN,
        starting_balances=[Money(10_000, Currency.from_str("USD"))],
        base_currency=Currency.from_str("USD"),
        default_leverage=Decimal(1),
        bar_adaptive_high_low_ordering=True,
    )

    activation_ns = metadata.start
    expiration_ns = metadata.end
    ts_event_ns = int(datetime.now(tz=UTC).timestamp() * 1_000_000_000)
    ts_init_ns = metadata.start

    instrument = FuturesContract(
        instrument_id=InstrumentId(symbol=symbol, venue=venue),
        raw_symbol=symbol,
        asset_class=AssetClass.INDEX,
        exchange="XCME",
        currency=USD,
        price_precision=2,
        price_increment=Price.from_str("0.01"),
        multiplier=Quantity.from_int(1),
        lot_size=Quantity.from_int(1),
        underlying="ES",
        activation_ns=activation_ns,
        expiration_ns=expiration_ns,
        ts_event=ts_event_ns,
        ts_init=ts_init_ns,
    )

    engine.add_instrument(instrument)
    engine.add_data(data)

    strategy_config = EMACrossConfig(
        instrument_id=instrument_id,
        bar_type=data[0].bar_type,
        trade_size=Decimal(100),
        fast_ema_period=fast_period,
        slow_ema_period=slow_period,
    )

    strategy = EMACross(config=strategy_config)
    engine.add_strategy(strategy=strategy)

    engine.run()

    timestamp = datetime.now(UTC).strftime("%Y-%m-%d_%H:%M:%S")
    filename = Path(config.results_path()) / f"{timestamp}.json"

    save_data(
        data=replace_nan_to_none(vars(engine.get_result())),
        file_path=Path(filename),
    )
