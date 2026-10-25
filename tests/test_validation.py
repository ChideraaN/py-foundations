import json

import pytest

from bag import Bag
from main import BASE_DIR, read_csv_to_dict, validate_bag_reports_csv, write_reports

@pytest.fixture
def rows():
    """Sample CSV rows by letter. Rebuilt for every test, so mutations don't leak between tests."""
    return {
        # valid
        "A": {"report_id": "T-001", "colour": "red", "bag_form": "suitcase", "shell": "hard", "brand": "Acme", "weight_kg": "20.5"},
        "B": {"report_id": "T-002", "colour": "blue", "bag_form": "backpack", "shell": "", "brand": "", "weight_kg": "7"},
        "C": {"report_id": "T-003", "colour": "green", "bag_form": "duffel", "shell": "soft", "brand": "Zed", "weight_kg": ""},
        "D": {"report_id": "T-004", "colour": "black", "bag_form": "suitcase", "shell": "hard", "brand": "Acme", "weight_kg": "0"},
        "E": {"report_id": "T-005", "colour": "white", "bag_form": "suitcase", "shell": "soft", "brand": "Acme", "weight_kg": "32"},
        # invalid
        "F": {"report_id": "T-006", "colour": "", "bag_form": "suitcase", "shell": "hard", "brand": "Acme", "weight_kg": "10"},
        "G": {"report_id": "T-007", "colour": "pink", "bag_form": "banana", "shell": "", "brand": "Acme", "weight_kg": "10"},
        "H": {"report_id": "T-008", "colour": "grey", "bag_form": "suitcase", "shell": "lukewarm", "brand": "Acme", "weight_kg": "10"},
        "I": {"report_id": "T-009", "colour": "tan", "bag_form": "duffel", "shell": "", "brand": "Acme", "weight_kg": "32.5"},
        "J": {"report_id": "T-010", "colour": "teal", "bag_form": "duffel", "shell": "", "brand": "Acme", "weight_kg": "-1"},
        "K": {"report_id": "T-011", "colour": "gold", "bag_form": "duffel", "shell": "", "brand": "Acme", "weight_kg": "heavy"},
        "L": {"report_id": "", "colour": "navy", "bag_form": "duffel", "shell": "", "brand": "Acme", "weight_kg": "10"},
    }

def test_read_csv_to_dict(rows):
    csv_rows = read_csv_to_dict(BASE_DIR / "tests/test_reports.csv")
    assert rows["A"] in csv_rows
    assert rows["B"] in csv_rows


def test_validate_bag_reports_csv(rows):
    inputs = [rows["A"], rows["B"], rows["H"]]
    valid, invalid = validate_bag_reports_csv(inputs)
    assert Bag(**rows["A"]) in valid
    assert Bag(**rows["B"]) in valid
    assert rows["H"] not in valid
    assert len(valid) == 2
    assert rows["H"] in invalid

def test_write_reports(tmp_path, rows):
    valid_path = tmp_path / "valid.json"
    rejects_path = tmp_path / "rejects.json"
    bad = [rows["F"], rows["G"], rows["H"]]
    write_reports(valid_path, rejects_path, [Bag(**rows["A"]), Bag(**rows["A"]), Bag(**rows["A"])], bad)

    assert len(json.loads(valid_path.read_text())) == 3
    assert json.loads(rejects_path.read_text()) == bad

@pytest.mark.parametrize("key", ["F", "G", "H", "I", "J", "K", "L"])
def test_invalid_rows(rows, key):
    valid, invalid = validate_bag_reports_csv([rows[key]])
    assert len(valid) == 0
    assert len(invalid) == 1

@pytest.mark.parametrize("key", ["A", "B", "C", "D", "E"])
def test_valid_rows(rows, key):
    valid, invalid = validate_bag_reports_csv([rows[key]])
    assert len(valid) == 1
    assert len(invalid) == 0

def test_milstone_numbers(tmp_path):
    rows = read_csv_to_dict(BASE_DIR / "bag_reports.csv")
    valid, invalid = validate_bag_reports_csv(rows)
    valid_path = tmp_path / "valid.json"
    rejects_path = tmp_path / "rejects.json"
    write_reports(valid_path, rejects_path, valid, invalid)

    assert len(json.loads(valid_path.read_text())) == 24
    assert len(json.loads(rejects_path.read_text())) == 6
    

