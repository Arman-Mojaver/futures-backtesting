import json
from pathlib import Path
from typing import Any


def save_data(data: dict[str, Any], file_path: Path) -> None:
    with file_path.open(mode="w+") as f:
        json.dump(data, f, indent=3, sort_keys=True)
