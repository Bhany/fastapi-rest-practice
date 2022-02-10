from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import DateTime
from db.base import Base

class Shipment(Base):
    __tablename__ = "shipment"

    id = Column(Integer, primary_key=True, index=True)
    reference_id = Column(String, index=True, nullable=False) 
    estimated_time_arrival = Column(DateTime, index=True, nullable=True) 
    transport_packs = relationship("Node", back_populates="shipments") # one to many
    organizations = relationship("Organization", secondary="ship_org", back_populates='shipments') # many to many

