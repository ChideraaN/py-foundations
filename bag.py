from typing import Literal, Optional
from pydantic import BaseModel, field_validator

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