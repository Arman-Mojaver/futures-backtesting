import sys
from pathlib import Path

import click

sys.path.append(Path(__file__).resolve().parent.parent.as_posix())


from .save_data import save
from .stats import stats


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
def main() -> None:
    pass


main.add_command(save)
main.add_command(stats)


if __name__ == "__main__":
    main()
