from datetime import UTC, datetime
from pathlib import Path

import click
from databento.common.dbnstore import DBNStore

from config import config


@click.command("stats", help="Show stats of the latest saved price data")
def stats() -> None:
    file_path = sorted(Path(config.price_data_path()).glob("*.dbn"))[-1]

    data = DBNStore.from_file(file_path)
    metadata = data.metadata

    click.echo(click.style("File:", bold=True, fg="blue") + f" {file_path}")
    click.echo(click.style("Metadata", bold=True, fg="cyan"))
    click.echo(f"  Version: {metadata.version}")
    click.echo(f"  Dataset: {metadata.dataset}")
    click.echo(f"  Schema: {metadata.schema}")
    click.echo(
        f"  Start: {metadata.start} "
        f"({datetime.fromtimestamp(metadata.start / 1e9, UTC):%Y-%m-%d})"
    )
    click.echo(
        f"  End: {metadata.end} "
        f"({datetime.fromtimestamp(metadata.end / 1e9, UTC):%Y-%m-%d})"
        if metadata.end else "  End: None"
    )
    click.echo(f"  Count: {len(list(data))}")
    click.echo(f"  Limit: {metadata.limit}")
    click.echo(f"  stype_in: {metadata.stype_in}")
    click.echo(f"  stype_out: {metadata.stype_out}")
    click.echo(f"  Symbols: {', '.join(metadata.symbols) if metadata.symbols else '[]'}")
    click.echo("")
    click.echo(click.style("Symbol Mappings", bold=True, fg="yellow"))

    for raw_symbol, intervals in metadata.mappings.items():
        click.echo(click.style(f"  Raw Symbol: {raw_symbol}", bold=True))
        click.echo(
            "    "
            + click.style(
                f"{'Symbol':<10} {'Start Date':<12} {'End Date':<12}",
                bold=True,
                underline=True,
            )
        )
        for interval in intervals:
            start = (
                interval.start_date
                if hasattr(interval, "start_date")
                else interval["start_date"]
            )
            end = (
                interval.end_date
                if hasattr(interval, "end_date")
                else interval["end_date"]
            )
            symbol = (
                interval.symbol if hasattr(interval, "symbol") else interval["symbol"]
            )

            click.echo(
                "    "
                + click.style(f"{symbol:<10}", fg="green")
                + f" {start:%Y-%m-%d}  {end:%Y-%m-%d}"
            )
        click.echo("")

    click.echo("")
