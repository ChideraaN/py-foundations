import csv
from typing import Optional
from pydantic.dataclasses import dataclass
from pydantic import Field, field_validator


path = "py-foundations/bag_reports.csv"
encoding = "utf-8"

with open(path, "r", encoding=encoding) as file:
    reader = csv.DictReader(file)
    rows = list(reader)

def is_empty(value):
    value is "";

@dataclass
class Bag():
    report_id: Field(exclude_if=is_empty())
    colour: Optional[str]
    bag_type: Optional[str]
    brand: Optional[str]
    weight_kg: Optional[float]

    # create field validator for report id

    @field_validator("weight_kg", mode="before")
    @classmethod
    def weight_is_not_empty_or_negative(cls, value):
        if(float(value) < 1):
            raise ValueError("Weight is empty or less than zero")
        return value

valid = []
invalid = 0

for x in range(len(rows)):
    try:
        bag = Bag(rows[x]["report_id"],rows[x]["colour"],rows[x]["bag_type"],rows[x]["brand"],rows[x]["weight_kg"])
        valid.append(bag)
    except ValueError as e:
        invalid+=1

print("Valid Bag", *valid, sep="\n")
print(len(valid))
print(invalid)
