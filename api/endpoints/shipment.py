from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from crud import crud_shipment as crud_ship
from schemas import shipment as schema_ship
from schemas import node as schema_node
from api.deps import get_db

router = APIRouter()

@router.post("/shipment/", status_code=201, response_model=schema_ship.Shipment)
def create_shipment(shipment: schema_ship.Shipment, db: Session = Depends(get_db)):
    db_shipment = crud_ship.get_shipment(db, referenceId=shipment.referenceId)
    if db_shipment:
        raise HTTPException(status_code=400, detail="Shipment already exists")
    return crud_ship.create_shipment(db=db, shipment=shipment)

@router.get("/shipments/", status_code=200, response_model=List[schema_ship.Shipment])
def read_shipments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    shipments = crud_ship.get_shipments(db, skip=skip, limit=limit)
    return shipments

@router.get("/shipments/{ref_id}", status_code=200, response_model=schema_ship.Shipment)
def read_shipment(ref_id: str, db: Session = Depends(get_db)):
    db_shipment = crud_ship.get_shipment(db, referenceId=ref_id)
    if db_shipment is None:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return db_shipment

@router.get("/shipments/aggregate/{unit}/", status_code=200, response_model=schema_node.NodeAggregate)
def aggregate_node_weights(unit: str, db: Session = Depends(get_db)):
    agg_node = crud_ship.aggregate_node_weights(db, unit)
    if agg_node is None:
        raise HTTPException(status_code=404, detail="Nodes are not found")
    return agg_node

""" TODO: could become useful when more nodes are added
@app.post("/shipments/{ref_id}/nodes/", response_model=schemas.Node)
def create_node_for_shipment(
    ref_id: str, node: schemas.NodeCreate, db: Session = Depends(get_db)
):
    return crud.create_shipment_node(db=db, node=node, referenceId=ref_id)
"""