from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from crud import crud_node
from schemas.node import Node as schema_node
from api.deps import get_db

router = APIRouter()


@router.get("/nodes/", status_code=200, response_model=List[schema_node])
def read_nodes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    nodes = crud_node.get_nodes(db, skip=skip, limit=limit)
    return nodes
