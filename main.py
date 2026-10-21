import csv
from typing import Optional
from pydantic.dataclasses import dataclass
from pydantic import BaseModel, Field, field_validator


path = "py-foundations/bag_reports.csv"
encoding = "utf-8"

with open(path, "r", encoding=encoding) as file:
    reader = csv.DictReader(file)
    rows = list(reader)



class Bag(BaseModel):
    report_id: str
    colour: str
    bag_form: str
    shell: str
    brand: Optional[str]
    weight_kg: Optional[float]

    @field_validator("report_id", "colour", "bag_form", "shell", mode="before")
    @classmethod
    def is_empty(cls, value):
        if(len(value) < 1):
            raise ValueError("Field is Empty")
        return value

    @field_validator("weight_kg", mode="before")
    @classmethod
    def weight_is_not_empty_or_negative(cls, value):
        if(float(value) < 1):
            value = None
        return value

valid = []
invalid = []

for x in range(len(rows)):
    try:
        bag = Bag(
            **rows[x]
        )

        valid.append(bag)
    except ValueError as e:
        invalid.append(bag)

print("Valid Bag", *valid, sep="\n")
print(len(valid))
print("Invalid Bag", *invalid, sep="\n")
print(len(invalid))
