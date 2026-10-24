import pytest
from pydantic import ValidationError
import math

from bag import Bag


@pytest.fixture
def row():
    """A valid CSV row; each test copies it and changes one field."""
    return {
        "report_id": "R-1001",
        "colour": "navy",
        "bag_form": "suitcase",
        "shell": "hard",
        "brand": "Samsonite",
        "weight_kg": "18.5",
    }


def test_valid_bag_is_created(row):
    bag = Bag(**row)
    assert bag.report_id == "R-1001"
    assert bag.colour == "navy"
    assert bag.weight_kg == 18.5


def test_invalid_bag_raises_error(row):
    row["report_id"]=" "
    with pytest.raises(ValidationError, match="Field is Empty"):
        bag = Bag(**row)
    

def test_whitespaces_are_stripped(row):
    row["colour"] = " navy "
    bag = Bag(**row)
    assert bag.colour == "navy"

def test_blanks_are_converted_to_none(row):
    row["brand"] = "  "
    bag = Bag(**row)
    assert bag.brand == None

@pytest.mark.parametrize("weight", ["400", "-10", "33"])
def test_too_large_or_negative_weight_not_allowed(row,weight):
    row["weight_kg"] = weight
    with pytest.raises(ValidationError, match="Weight is negative or too large"):
        bag = Bag(**row)

@pytest.mark.parametrize("weight", [math.nan, None, "abc"])
def test_non_number_values_not_allowed(row, weight):
    row["weight_kg"] = weight
    with pytest.raises(ValidationError, match="Weight is not a number"):
        bag = Bag(**row)

