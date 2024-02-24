import json
import os
from datetime import datetime
from pathlib import Path

from botasaurus import bt


def write_file(*, data: dict, file_path: str | Path) -> None:
    """
    Save the data as a JSON file in output/*.json

    :param data: The data to be written to the file
    :param file_path: Directory
    """
    print("Writing")
    print("\t" + str(file_path))

    try:
        with open(file_path, "r") as file:
            content = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        content = []

    new_offer = {
        "datetime": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        "main_offer": data,
    }

    # Compare new_offer with existing offers
    if all(
        new_offer["main_offer"] != existing_offer["main_offer"]
        for existing_offer in content
    ):
        # Append new_offer if it does not exist in content
        content.append(new_offer)

    with open(file_path, "w") as file:
        json.dump(content, file, indent=4)


def read_main_offer() -> None:
    """
    Reads the main offer from a JSON file and prints it with indentation.
    """
    print("Reading last offer")
    file_name = os.getenv("FILENAME")
    print(json.dumps(bt.read_json(file_name)[-1], indent=4, ensure_ascii=False))
