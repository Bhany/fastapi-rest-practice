from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
import datetime as dt

class total_weight(BaseModel):
    weight: float
    unit: str


class Node(BaseModel):
    total_weight: total_weight
    class Config:
        orm_mode = True


class NodeAggregate(BaseModel):
    count: int
    weight: float
    unit: str


class TransportPacks(BaseModel):
    nodes: List[Node]
    class Config:
        orm_mode = True


class Shipment(BaseModel):
    type: str
    reference_id: str
    estimated_time_arrival: Optional[dt.datetime]
    transport_packs: TransportPacks
    class Config:
        orm_mode = True


class Organization(BaseModel):
    type: str
    id: UUID
    code: str

    class Config:
        orm_mode = True


class ShipmentSchema(Shipment):
    organizations: List[str]


class OrganizationSchema(Organization):
    shipments: List[Shipment]