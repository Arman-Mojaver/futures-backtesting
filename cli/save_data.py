import datetime
from pathlib import Path

import click

from config import config
from src.databento_client import DatabentoClient
from src.dataframe_utils import from_databento_df_to_items
from src.utils import save_data


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
    dataframe = client.get_range(
        start_date=start_date,
        end_date=end_date,
        limit=limit,
    )
    data = from_databento_df_to_items(dataframe)
    timestamp = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d_%H:%M:%S")
    filename = Path(config.price_data_path()) / f"{timestamp}.json"
    save_data(data=data, file_path=Path(filename))

    click.echo(f"Saved {len(data)} data points from Databento. File: {filename}")
