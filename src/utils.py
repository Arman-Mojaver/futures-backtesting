import json
import math
from pathlib import Path
from typing import Any


def save_data(data: dict[str, Any], file_path: Path) -> None:
    with file_path.open(mode="w+") as f:
        json.dump(data, f, indent=3, sort_keys=True)


def replace_nan_to_none(obj: object) -> object:
    if isinstance(obj, dict):
        return {k: replace_nan_to_none(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [replace_nan_to_none(v) for v in obj]
    if isinstance(obj, float) and math.isnan(obj):
        return None
    return obj
