from enum import Enum

class WeightUnit(str, Enum):
    kg = "KILOGRAMS"
    lb = "POUNDS"
    oz = "OUNCES"

class WeightConverter:
    def __init__(self):
        self.kg_to_lb = 2.20462
        self.kg_to_oz = 35.274
        self.lb_to_kg = 0.453592
        self.lb_to_oz = 16
        self.oz_to_kg = 0.0283495
        self.oz_to_lb = 0.0625

    def convert(self, weight, original_unit):
        if original_unit == "OUNCES":
            return {'kg': weight*self.oz_to_kg, 'lb': weight*self.oz_to_lb, 'oz':weight}
        if original_unit == "POUNDS":
            return {'kg': weight*self.lb_to_kg, 'lb': weight, 'oz': weight*self.lb_to_oz}
        if original_unit == "KILOGRAMS":
            return {'kg': weight, 'lb': weight*self.kg_to_lb, 'lb': weight*self.kg_to_oz}
    


