from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from crud import crud_node
from schemas import node as schema_node
from api.deps import get_db

router = APIRouter()


@router.get("/nodes/aggregate/{unit}/", status_code=200, response_model=schema_node.NodeAggregate)
def aggregate_node_weights(unit: str, db: Session = Depends(get_db)):
    agg_node = crud_node.aggregate_node_weights(db, unit)
    if not agg_node:
        raise HTTPException(status_code=404, detail="Nodes are not found")
    return agg_node

@router.get("/nodes/", status_code=200, response_model=List[schema_node.Node])
def read_nodes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    nodes = crud_node.get_nodes(db, skip=skip, limit=limit)
    if not nodes:
        raise HTTPException(status_code=404, detail="Nodes are not found")
    return nodes

