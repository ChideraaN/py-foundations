import csv
import json
from pathlib import Path

from bag import Bag

# Folder that contains this script, so paths work no matter where it is run from
BASE_DIR = Path(__file__).parent

# Input CSV and output JSON files all live next to main.py
CSV_PATH = BASE_DIR / "bag_reports.csv"
VALID_PATH = BASE_DIR / "valid.json"
REJECTS_PATH = BASE_DIR / "rejects.json"

# open() accepts a Path object directly
with open(CSV_PATH, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    rows = list(reader)

def validate_bag_reports_csv(valid: list, invalid: list):
    for x in range(len(rows)):
        try:
            bag = Bag(**rows[x])
            valid.append(bag)
        except ValueError as e:
            rows[x]["failure_reason"] = str(e)
            invalid.append(rows[x])

    return valid, invalid

def write_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def write_reports(valid: list, invalid: list):
    write_json("py-foundations/valid.json", [report.model_dump() for report in valid])
    write_json("py-foundations/rejects.json", invalid)


# valid, invalid = validate_bag_reports_csv([], [])
# write_reports(valid, invalid)
