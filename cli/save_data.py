import click


@click.command("save", help="Load Databento data and save it in json format")
def save_data() -> None:
    print("Loading data from Databento")  # noqa: T201
