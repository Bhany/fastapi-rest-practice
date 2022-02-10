from sqlalchemy import schema
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from crud import crud_shipment as crud_ship
from schemas import schemas
from api.deps import get_db

router = APIRouter()

@router.post("/shipment/", status_code=201, response_model=schemas.ShipmentSchema)
def create_shipment(shipment: schemas.ShipmentSchema, db: Session = Depends(get_db)):
    return crud_ship.create_shipment(db=db, shipment=shipment)


@router.get("/shipments/", status_code=200, response_model=List[schemas.ShipmentSchema])
def read_shipments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_ship.get_shipments(db, skip=skip, limit=limit)


@router.get("/shipments/{ref_id}", status_code=200, response_model=schemas.ShipmentSchema)
def read_shipment(ref_id: str, db: Session = Depends(get_db)):
    return crud_ship.get_shipment(db, reference_id=ref_id)


""" TODO: could become useful when more nodes are added
@app.post("/shipments/{ref_id}/nodes/", response_model=schemas.Node)
def create_node_for_shipment(
    ref_id: str, node: schemas.NodeCreate, db: Session = Depends(get_db)
):
    return crud.create_shipment_node(db=db, node=node, reference_id=ref_id)
"""