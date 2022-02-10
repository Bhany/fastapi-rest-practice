from enum import Enum
from fastapi import HTTPException
from typing import Final

class MessageType(str, Enum):
    org = "ORGANIZATION"
    ship = "SHIPMENT"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_ 


class WeightUnit(str, Enum):
    kg = "KILOGRAMS"
    lb = "POUNDS"
    oz = "OUNCES"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_ 


class WeightConversion():
    kg_to_lb: Final[float] = 2.20462
    kg_to_oz: Final[float] = 35.274
    lb_to_kg: Final[float] = 0.453592
    lb_to_oz: Final[float] = 16
    oz_to_kg: Final[float] = 0.0283495
    oz_to_lb: Final[float] = 0.0625


class WeightConverter:
    @staticmethod
    def convert(weight, unit):
        if not WeightUnit.has_value(unit): 
            raise HTTPException(status_code=404, detail="Unit not supported")
        if weight < 0: 
            raise HTTPException(status_code=404, detail="Negative weight not supported")

        if unit == WeightUnit.oz:
            return {'kg': weight*WeightConversion.oz_to_kg, 'lb': weight*WeightConversion.oz_to_lb, 'oz':weight}
        elif unit == WeightUnit.lb:
            return {'kg': weight*WeightConversion.lb_to_kg, 'lb': weight, 'oz': weight*WeightConversion.lb_to_oz}
        elif unit == WeightUnit.kg:
            return {'kg': weight, 'lb': weight*WeightConversion.kg_to_lb, 'oz': weight*WeightConversion.kg_to_oz}