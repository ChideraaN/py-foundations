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
    assert len(csv_rows) == 2
    assert rows["A"] in csv_rows
    assert rows["B"] in csv_rows


def test_validate_bag_reports_csv(rows):
    inputs = [rows["A"], rows["B"], rows["H"]]
    valid, invalid = validate_bag_reports_csv(inputs)
    assert valid == [Bag(**rows["A"]), Bag(**rows["B"])]
    assert len(invalid) == 1
    assert invalid[0]["report_id"] == "T-008"
    assert "shell" in invalid[0]["failure_reason"]


def test_write_reports(tmp_path, rows):
    valid_path = tmp_path / "valid.json"
    rejects_path = tmp_path / "rejects.json"
    good = [Bag(**rows["A"]), Bag(**rows["B"])]
    bad = [rows["F"], rows["G"], rows["H"]]
    write_reports(valid_path, rejects_path, good, bad)

    assert json.loads(valid_path.read_text()) == [bag.model_dump() for bag in good]
    assert json.loads(rejects_path.read_text()) == bad


@pytest.mark.parametrize("key, expected", [
    ("F", "Field is Empty"),
    ("G", "bag_form"),
    ("H", "shell"),
    ("I", "negative or too large"),
    ("J", "negative or too large"),
    ("K", "not a number"),
    ("L", "Field is Empty"),
])
def test_invalid_rows(rows, key, expected):
    valid, invalid = validate_bag_reports_csv([rows[key]])
    assert len(valid) == 0
    assert len(invalid) == 1
    assert expected in invalid[0]["failure_reason"]


@pytest.mark.parametrize("key, expected", [
    ("A", {"shell": "hard", "brand": "Acme", "weight_kg": 20.5}),
    ("B", {"shell": None, "brand": None, "weight_kg": 7.0}),
    ("C", {"shell": "soft", "brand": "Zed", "weight_kg": None}),
    ("D", {"shell": "hard", "brand": "Acme", "weight_kg": 0.0}),
    ("E", {"shell": "soft", "brand": "Acme", "weight_kg": 32.0}),
])
def test_valid_rows(rows, key, expected):
    valid, invalid = validate_bag_reports_csv([rows[key]])
    assert len(invalid) == 0
    assert len(valid) == 1
    bag = valid[0]
    assert bag.report_id == rows[key]["report_id"]
    for field, value in expected.items():
        assert getattr(bag, field) == value


def test_milestone_numbers(tmp_path):
    csv_rows = read_csv_to_dict(BASE_DIR / "bag_reports.csv")
    valid, invalid = validate_bag_reports_csv(csv_rows)
    valid_path = tmp_path / "valid.json"
    rejects_path = tmp_path / "rejects.json"
    write_reports(valid_path, rejects_path, valid, invalid)

    valid_ids = {r["report_id"] for r in json.loads(valid_path.read_text())}
    rejected_ids = {r["report_id"] for r in json.loads(rejects_path.read_text())}

    assert len(valid_ids) == 24
    assert rejected_ids == {"R-1025", "R-1026", "R-1027", "R-1028", "R-1029", ""}
    assert valid_ids.isdisjoint(rejected_ids)
