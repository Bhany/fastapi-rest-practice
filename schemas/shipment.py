from pydantic import BaseModel
from enum import Enum
from typing import Optional, List

# type of query message
class QueryGetType(str, Enum):
    shipment = "shipments"
    organization = "organizations"
    extra = "extra"

class Organization(BaseModel):
    organization: str
    code: str

class WeightUnit(str, Enum):
    lb: str = 'POUNDS'
    kg: str = 'KILOGRAMs'

class Total_Weight(BaseModel):
    weight: float # type check
    unit: WeightUnit

class Transport_Packs(BaseModel):
    nodes: Optional[List[Total_Weight]] = []

class Shipment(BaseModel):
    reference_id: str
    organization: Optional[List[Organization]] = [] # can be empty list
    estimated_time_arrival: Optional[str] = None # will need to be checked
    transport_packs: Transport_Packs


