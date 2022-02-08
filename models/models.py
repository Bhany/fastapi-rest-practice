from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import DateTime

from db.db import Base

class Organization(Base):
    __tablename__ = "organization"

    id = Column(String, primary_key=True, index=True)
    code = Column(String, unique=True, index=True)
    shipment_ids = Column(String, ForeignKey("shipment.referenceId"))

    shipments = relationship("Shipment", back_populates="organizations")

   
class Shipment(Base):
    __tablename__ = "shipment"

    id = Column(Integer, primary_key=True, index=True)
    referenceId = Column(String, index=True) 
    organizations = relationship("Organization", back_populates="shipments")    
    estimatedTimeArrival = Column(DateTime, index=True, nullable=True) 
    node_id = Column(String, ForeignKey("node.id"))

    #transportPacks = relationship("Node", back_populates="shipment")


class Node(Base):
    __tablename__ = "node"

    id = Column(Integer, primary_key=True, index=True)
    weight = Column(Float, index=True)
    original_unit = Column(String, index=True)
    kg = Column(Float, index=True)
    oz = Column(Float, index=True)
    lb = Column(Float, index=True)
    owner_id = Column(String, ForeignKey("shipment.referenceId"))
    #shipment = relationship("Shipment", back_populates="transportPacks")
