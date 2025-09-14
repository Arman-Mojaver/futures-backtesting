import click


@click.command("load", help="Load Databento data and save it in json format")
def load_data() -> None:
    print("Loading data from Databento")  # noqa: T201
