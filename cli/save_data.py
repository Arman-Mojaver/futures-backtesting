import datetime
from pathlib import Path

import click

from config import config
from src.databento_client import DatabentoClient


@click.option(
    "-s",
    "--start_date",
    default="2024-01-01",
    type=str,
    help="Start date (format: YYYY-MM-DD,  default: 2024-01-01)",
)
@click.option(
    "-e",
    "--end_date",
    default="2024-01-02",
    type=str,
    help="End date (format: YYYY-MM-DD, default: 2024-01-02)",
)
@click.option(
    "-l",
    "--limit",
    default=1,
    type=int,
    help="Limit (default: 1)",
)
@click.command("save", help="Load Databento data and save it in json format")
def save(start_date: str, end_date: str, limit: int) -> None:
    click.echo("Loading data from Databento")

    client = DatabentoClient(api_key=config.DATABENTO_API_KEY)
    try:
        data = client.get_range(
            start_date=start_date,
            end_date=end_date,
            limit=limit,
        )
    except Exception as e:  # noqa: BLE001
        click.echo(f"Unable to retrieve data from Databento: {e}")
        return

    timestamp = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d_%H:%M:%S")
    filename = Path(config.price_data_path()) / f"{timestamp}.dbn"
    data.to_file(filename)

    click.echo(f"Saved {len(list(data))} data points from Databento. File: {filename}")
