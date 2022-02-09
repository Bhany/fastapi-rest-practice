from models import node 
from models import organization
from models import shipment
from db.base import SessionLocal, engine

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

node.Base.metadata.create_all(bind=engine)
organization.Base.metadata.create_all(bind=engine)
shipment.Base.metadata.create_all(bind=engine)

