from sqlalchemy import Column, ForeignKey, Integer, String, Float

from db.base import Base

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
