from pydantic import BaseModel
from typing import Optional, List
import uuid 
import datetime as dt


class Organization(BaseModel):
    id: uuid.UUID
    code: str
    class Config:
        orm_mode = True

class OrganizationCreate(Organization):
    pass

class totalWeight(BaseModel):
    weight: float # type check
    unit: str

class Node(BaseModel):
    totalWeight: totalWeight
    class Config:
        orm_mode = True

class NodeCreate(Node):
    pass

class TransportPacks(BaseModel):
    nodes: List[Node]
    class Config:
        orm_mode = True

class Shipment(BaseModel):
    referenceId: str
    organizations: List[str]
    estimatedTimeArrival: Optional[dt.datetime]
    transportPacks: TransportPacks
    class Config:
        orm_mode = True

class ShipmentCreate(Shipment):
    pass
