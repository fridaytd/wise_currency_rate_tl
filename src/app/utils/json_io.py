import json
from pathlib import Path


def read_json(
    path: Path,
) -> list | dict:
    with open(path) as f:
        data = json.load(f)

    return data
