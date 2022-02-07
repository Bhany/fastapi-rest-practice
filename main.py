from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from crud import crud
from models import models
from schemas import schemas
from db.db import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/shipment/", response_model=schemas.Shipment)
def create_shipment(shipment: schemas.ShipmentCreate, db: Session = Depends(get_db)):
    db_shipment = crud.get_shipment(db, referenceId=shipment.referenceId)
    if db_shipment:
        raise HTTPException(status_code=400, detail="Shipment already exists")
    return crud.create_shipment(db=db, shipment=shipment)

@app.post("/organization/", response_model=schemas.Organization)
def create_organization(organization: schemas.OrganizationCreate, db: Session = Depends(get_db)):
    db_organization = crud.get_organization(db, id=organization.id)
    if db_organization:
        raise HTTPException(status_code=400, detail="Organization already exists")
    return crud.create_organization(db=db, organization=organization)

@app.get("/shipments/", response_model=List[schemas.Shipment])
def read_shipments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    shipments = crud.get_shipments(db, skip=skip, limit=limit)
    return shipments

@app.get("/organizations/", response_model=List[schemas.Organization])
def read_organizations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    organizations = crud.get_organizations(db, skip=skip, limit=limit)
    return organizations

@app.get("/shipments/{ref_id}", response_model=schemas.Shipment)
def read_shipment(ref_id: str, db: Session = Depends(get_db)):
    db_shipment = crud.get_shipment(db, referenceId=ref_id)
    if db_shipment is None:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return db_shipment

@app.get("/organizations/id/{id}", response_model=schemas.Organization)
def read_organization(id: str, db: Session = Depends(get_db)):
    db_organization = crud.get_organization(db, id=id)
    if db_organization is None:
        raise HTTPException(status_code=404, detail="Organization not found")
    return db_organization

@app.get("/organizations/code/{code}", response_model=schemas.Organization)
def read_organization_by_code(code: str, db: Session = Depends(get_db)):
    db_organization = crud.get_organization_by_code(db, code=code)
    if db_organization is None:
        raise HTTPException(status_code=404, detail="Organization not found")
    return db_organization


@app.get("/nodes/", response_model=List[schemas.Node])
def read_nodes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    nodes = crud.get_nodes(db, skip=skip, limit=limit)
    return nodes

"""
@app.post("/shipments/{ref_id}/nodes/", response_model=schemas.Node)
def create_node_for_shipment(
    ref_id: str, node: schemas.NodeCreate, db: Session = Depends(get_db)
):
    return crud.create_shipment_node(db=db, node=node, referenceId=ref_id)
"""
