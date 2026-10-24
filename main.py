import csv
import json
import sys
from pathlib import Path

from bag import Bag

# Folder that contains this script, so paths work no matter where it is run from
BASE_DIR = Path(__file__).parent

# Input CSV and output JSON files all live next to main.py
CSV_PATH = BASE_DIR / "bag_reports.csv"
VALID_PATH = BASE_DIR / "valid.json"
REJECTS_PATH = BASE_DIR / "rejects.json"

# open() accepts a Path object directly
def read_csv_to_dict(path_to_file):
    with open(path_to_file, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        return rows

def validate_bag_reports_csv(rows: list):
    valid = []
    invalid = []
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

def write_reports(valid_path, rejects_path, valid, invalid):
    write_json(valid_path, [report.model_dump() for report in valid])
    write_json(rejects_path, invalid)


def main():
    rows = read_csv_to_dict(CSV_PATH)
    valid, invalid = validate_bag_reports_csv(rows)
    write_reports(VALID_PATH, REJECTS_PATH, valid, invalid)

if __name__ == "__main__":
    sys.exit(main()) 