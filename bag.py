import math
from typing import Literal, Optional
from pydantic import BaseModel, field_validator

class Bag(BaseModel):
    report_id: str
    colour: str
    bag_form: Literal["suitcase", "backpack", "duffel"]
    shell: Optional[Literal["hard", "soft"]]
    brand: Optional[str]
    weight_kg: Optional[float]

    @field_validator("report_id", "colour", "bag_form", mode="before")
    @classmethod
    def is_empty_or_invalid(cls, value):
        # None and whitespace-only strings count as empty, not just ""
        if value is None or (isinstance(value, str) and not value.strip()):
            raise ValueError("Field is Empty")
        return value.strip() if isinstance(value, str) else value

    @field_validator("shell", "brand", "weight_kg", mode="before")
    @classmethod
    def blank_to_none(cls, value):
        # Optional fields: a blank cell means "no value", stored as None
        if value is None or (isinstance(value, str) and not value.strip()):
            return None
        return value.strip() if isinstance(value, str) else value

    @field_validator("weight_kg", mode="before")
    @classmethod
    def weight_is_not_too_large_or_negative(cls, value):
        if str(value).strip() == "":
            return None

        try:
            weight = float(value)
        except (TypeError, ValueError):
            raise ValueError("Weight is not a number")

        if math.isnan(weight):
            raise ValueError("Weight is not a number")

        if(weight < 0 or weight > 32):
            raise ValueError("Weight is negative or too large")
        return weight
