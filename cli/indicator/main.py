import click

from .ema_cross import ema_cross


@click.group(name="indicator", help="Indicators")
def indicator_subcommands() -> None:
    pass


indicator_subcommands.add_command(ema_cross)
