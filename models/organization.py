from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from db.base import Base

class Organization(Base):
    __tablename__ = "organization"

    id = Column(String, primary_key=True, index=True)
    code = Column(String, unique=True, index=True)
    
    shipments = relationship("Shipment", secondary="ship_org", back_populates="organizations")

