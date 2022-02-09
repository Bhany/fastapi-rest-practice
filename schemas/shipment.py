from pydantic import BaseModel
from typing import Optional, List
from .node import Node

import datetime as dt

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
