from pydantic import BaseModel

class TotalWeight(BaseModel):
    weight: float # type check
    unit: str

class Node(BaseModel):
    totalWeight: TotalWeight
    class Config:
        orm_mode = True

class NodeCreate(Node):
    pass

class NodeAggregate(BaseModel):
    count: int
    weight: float
    unit: str