from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from db.base import Base

class Node(Base):
    __tablename__ = "node"

    id = Column(Integer, primary_key=True, index=True)
    weight = Column(Float, nullable=False)
    unit = Column(String, nullable=False)
    kg = Column(Float, nullable=False)
    oz = Column(Float, nullable=False)
    lb = Column(Float, nullable=False)
    shipment_id = Column(String, ForeignKey('shipment.reference_id'))
    shipments = relationship("Shipment", back_populates="transport_packs")
