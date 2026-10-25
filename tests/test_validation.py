import json

import pytest

from bag import Bag
from main import BASE_DIR, read_csv_to_dict, validate_bag_reports_csv, write_reports

# valid
ROW_A = {"report_id": "T-001", "colour": "red", "bag_form": "suitcase", "shell": "hard", "brand": "Acme", "weight_kg": "20.5"}
ROW_B = {"report_id": "T-002", "colour": "blue", "bag_form": "backpack", "shell": "", "brand": "", "weight_kg": "7"}
ROW_C = {"report_id": "T-003", "colour": "green", "bag_form": "duffel", "shell": "soft", "brand": "Zed", "weight_kg": ""}
ROW_D = {"report_id": "T-004", "colour": "black", "bag_form": "suitcase", "shell": "hard", "brand": "Acme", "weight_kg": "0"}
ROW_E = {"report_id": "T-005", "colour": "white", "bag_form": "suitcase", "shell": "soft", "brand": "Acme", "weight_kg": "32"}
# invalid
ROW_F = {"report_id": "T-006", "colour": "", "bag_form": "suitcase", "shell": "hard", "brand": "Acme", "weight_kg": "10"}
ROW_G = {"report_id": "T-007", "colour": "pink", "bag_form": "banana", "shell": "", "brand": "Acme", "weight_kg": "10"}
ROW_H = {"report_id": "T-008", "colour": "grey", "bag_form": "suitcase", "shell": "lukewarm", "brand": "Acme", "weight_kg": "10"}
ROW_I = {"report_id": "T-009", "colour": "tan", "bag_form": "duffel", "shell": "", "brand": "Acme", "weight_kg": "32.5"}
ROW_J = {"report_id": "T-010", "colour": "teal", "bag_form": "duffel", "shell": "", "brand": "Acme", "weight_kg": "-1"}
ROW_K = {"report_id": "T-011", "colour": "gold", "bag_form": "duffel", "shell": "", "brand": "Acme", "weight_kg": "heavy"}
ROW_L = {"report_id": "", "colour": "navy", "bag_form": "duffel", "shell": "", "brand": "Acme", "weight_kg": "10"}

@pytest.fixture
def test_rows():
    return [ROW_A, ROW_B, ROW_C, ROW_D, ROW_D, ROW_E, ROW_F, ROW_G, ROW_H, ROW_I, ROW_J, ROW_K, ROW_L]

def test_read_csv_to_dict():
    rows = read_csv_to_dict(BASE_DIR / "tests/test_reports.csv")
    assert rows.__contains__(ROW_A)
    assert rows.__contains__(ROW_B)


def test_validate_bag_reports_csv():
    rows = [ROW_A, ROW_B, ROW_H]
    valid, invalid = validate_bag_reports_csv(rows)
    print(valid)
    assert Bag(**ROW_A) in valid
    assert Bag(**ROW_B) in valid
    assert ROW_H not in valid
    assert len(valid) == 2
    assert ROW_H in invalid

def test_write_reports(tmp_path):
    valid_path = tmp_path / "valid.json"
    rejects_path = tmp_path / "rejects.json"
    write_reports(valid_path, rejects_path, [Bag(**ROW_A), Bag(**ROW_A), Bag(**ROW_A)], [ROW_F, ROW_G, ROW_H])

    assert len(json.loads(valid_path.read_text())) == 3
    assert json.loads(rejects_path.read_text()) == [ROW_F, ROW_G, ROW_H]
