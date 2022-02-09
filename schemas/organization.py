from pydantic import BaseModel
import uuid 

class Organization(BaseModel):
    type: str
    id: uuid.UUID
    code: str
    class Config:
        orm_mode = True

class OrganizationCreate(Organization):
    pass
