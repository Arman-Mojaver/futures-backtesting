import json
from pathlib import Path

import pytest

from config import config
from src.utils import save_data


def read_json(p: Path) -> dict:
    with p.open("r") as f:
        return json.load(f)


@pytest.fixture(autouse=True)
def clean_data_dir(data_dir: Path):
    for p in data_dir.iterdir():
        if p.is_file():
            p.unlink()

    yield

    for p in data_dir.iterdir():
        if p.is_file():
            p.unlink()


@pytest.fixture
def data_dir(tmp_path: Path) -> Path:
    return Path(config.price_data_path())


@pytest.fixture
def file_path(data_dir: Path) -> Path:
    return data_dir / "output.json"


@pytest.fixture
def random_data():
    return {"a": 1, "b": "text"}


def test_save_creates_file_when_folder_empty(file_path, random_data):
    save_data(random_data, file_path)

    assert file_path.exists()
    assert read_json(file_path) == random_data


def test_save_writes_with_existing_other_json_in_folder(data_dir, file_path, random_data):
    other = data_dir / "other.json"
    other_data = {"x": 9}
    with other.open("w") as f:
        json.dump(other_data, f)

    save_data(random_data, file_path)

    assert other.exists()
    assert read_json(other) == other_data
    assert file_path.exists()
    assert read_json(file_path) == random_data


def test_save_overwrites_existing_file(file_path, random_data):
    original = {"a": 2, "b": "other text"}
    with file_path.open("w") as f:
        json.dump(original, f)

    save_data(random_data, file_path)

    assert file_path.exists()
    assert read_json(file_path) == random_data
