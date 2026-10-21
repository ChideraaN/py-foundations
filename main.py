import csv
from typing import Literal, Optional
from pydantic.dataclasses import dataclass
from pydantic import BaseModel, Field, field_validator
import json

path = "py-foundations/bag_reports.csv"
encoding = "utf-8"

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

with open(path, "r", encoding=encoding) as file:
    reader = csv.DictReader(file)
    rows = list(reader)

def validate_bag_reports_csv():
    for x in range(len(rows)):
        try:
            bag = Bag(**rows[x])
            valid_bag_reports.append(bag)
        except ValueError as e:
            rows[x]["failure_reason"] = str(e)
            invalid_bag_reports.append(rows[x])

def write_json(path, data):
    with open(path, "w", encoding=encoding) as f:
        json.dump(data, f, indent=2)


def write_reports(valid, rejects):
    write_json("valid.json", [report.model_dump() for report in valid])
    write_json("rejects.json", rejects)


validate_bag_reports_csv()
write_reports(valid_bag_reports, invalid_bag_reports)
