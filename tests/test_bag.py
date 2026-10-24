import pytest
from pydantic import ValidationError

from bag import Bag


@pytest.fixture
def row():
    """A fresh valid row for each test”"""
    return {
        "report_id": "R-1001",
        "colour": "navy",
        "bag_form": "suitcase",
        "shell": "hard",
        "brand": "Samsonite",
        "weight_kg": "18.5",
    }

def test_invalid_bag_form_raises(row):
    with pytest.raises(ValidationError):
        row['bag_form'] = "banana"
        Bag(**row)
        
def test_valid_bag_is_created(row):
    bag = Bag(**row)
    assert bag.report_id == "R-1001"
    assert bag.colour == "navy"
    assert bag.weight_kg == 18.5

def test_whitespaces_are_stripped(row):
    row["colour"] = " navy "
    bag = Bag(**row)
    assert bag.colour == "navy"

@pytest.mark.parametrize("field", ["shell", "brand", "weight_kg"])
def test_blanks_are_converted_to_none(row, field):
    row[field] = "  "
    bag = Bag(**row)
    assert getattr(bag, field) is None

@pytest.mark.parametrize("weight", ["400", "-10", "33"])
def test_too_large_or_negative_weight_not_allowed(row,weight):
    row["weight_kg"] = weight
    with pytest.raises(ValidationError, match="Weight is negative or too large"):
        Bag(**row)

@pytest.mark.parametrize("weight", ["nan", None, "abc"])
def test_non_number_values_not_allowed(row, weight):
    row["weight_kg"] = weight
    with pytest.raises(ValidationError, match="Weight is not a number"):
        Bag(**row)

@pytest.mark.parametrize("field", ["report_id", "colour", "bag_form"])
def test_invalid_bag_raises_error(row, field):
    row[field]= " "
    with pytest.raises(ValidationError, match="Field is Empty"):
        Bag(**row)