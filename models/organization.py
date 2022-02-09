from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from db.base import Base

class Organization(Base):
    __tablename__ = "organization"

    id = Column(String, primary_key=True, index=True)
    code = Column(String, unique=True, index=True)
    shipment_ids = Column(String, ForeignKey("shipment.referenceId"))

    shipments = relationship("Shipment", back_populates="organizations")
