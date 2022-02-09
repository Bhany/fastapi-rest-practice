from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import DateTime

from db.base import Base

class Shipment(Base):
    __tablename__ = "shipment"

    id = Column(Integer, primary_key=True, index=True)
    referenceId = Column(String, index=True) 
    organizations = relationship("Organization", back_populates="shipments")    
    estimatedTimeArrival = Column(DateTime, index=True, nullable=True) 
    node_id = Column(String, ForeignKey("node.id"))