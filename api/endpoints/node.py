from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from crud import crud_node
from schemas import schemas
from api.deps import get_db

router = APIRouter()

@router.get("/nodes/aggregate/{unit}/", status_code=200, response_model=schemas.NodeAggregate)
def aggregate_node_weights(unit: str, db: Session = Depends(get_db)):
    return crud_node.aggregate_node_weights(db, unit)

@router.get("/nodes/", status_code=200, response_model=List[schemas.Node])
def read_nodes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_node.get_nodes(db, skip=skip, limit=limit)

