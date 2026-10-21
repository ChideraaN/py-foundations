import csv
from typing import Literal, Optional
from pydantic.dataclasses import dataclass
from pydantic import BaseModel, Field, field_validator
import json

path = "py-foundations/bag_reports.csv"
encoding = "utf-8"

with open(path, "r", encoding=encoding) as file:
    reader = csv.DictReader(file)
    rows = list(reader)

class Bag(BaseModel):
    report_id: str
    colour: str
    bag_form: Literal["suitcase", "backpack", "duffel"]
    shell: Optional[str]
    brand: Optional[str]
    weight_kg: Optional[float]

    @field_validator("report_id", "colour", "bag_form", mode="before")
    @classmethod
    def is_empty(cls, value):
        if(len(value) < 1):
            raise ValueError("Field is Empty")
        return value

    @field_validator("weight_kg", mode="before")
    @classmethod
    def weight_is_not_too_large_or_negative(cls, value):
        if str(value).strip() == "":
            return None

        if(float(value) < 0 or float(value) > 32):
            raise ValueError("Weight is negative or too large")
        return value

valid_bag_reports = []
invalid_bag_reports = []

for x in range(len(rows)):
    try:
        bag = Bag(**rows[x])
        valid_bag_reports.append(bag)
    except ValueError as e:
        rows[x]["failure_reason"] = str(e)
        invalid_bag_reports.append(rows[x])

with open("valid.json", "w", encoding=encoding) as f:
    json.dump([report.model_dump() for report in valid_bag_reports], f, indent=2)

with open("rejects.json", "w", encoding=encoding) as f:
    json.dump(invalid_bag_reports, f, indent=2)