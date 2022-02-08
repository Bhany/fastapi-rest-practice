from enum import Enum
from pydantic import BaseModel
from typing import Optional, List, Union
import uuid 
import datetime as dt

class WeightUnit(str, Enum):
    kg = "KILOGRAMS"
    lb = "POUNDS"
    oz = "OUNCES"

class Organization(BaseModel):
    type: str
    id: uuid.UUID
    code: str
    class Config:
        orm_mode = True

class OrganizationCreate(Organization):
    pass

class TotalWeight(BaseModel):
    weight: float # type check
    unit: str

class Node(BaseModel):
    totalWeight: TotalWeight
    class Config:
        orm_mode = True

class NodeCreate(Node):
    pass

class TransportPacks(BaseModel):
    nodes: List[Node]
    class Config:
        orm_mode = True

class Shipment(BaseModel):
    type: str
    referenceId: str
    organizations: List[str]
    estimatedTimeArrival: Optional[dt.datetime]
    transportPacks: TransportPacks
    class Config:
        orm_mode = True

class ShipmentCreate(Shipment):
    pass

class NodeAggregate(BaseModel):
    count: int
    weight: float
    unit: str