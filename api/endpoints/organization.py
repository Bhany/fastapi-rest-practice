from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from crud import crud_organization as crud_org
from schemas.organization import Organization as schema_org
from api.deps import get_db

router = APIRouter()

@router.post("/organization/", status_code=201, response_model=schema_org)
def create_organization(organization: schema_org, db: Session = Depends(get_db)):
    return crud_org.create_organization(db=db, organization=organization)

@router.get("/organizations/", status_code=200, response_model=List[schema_org])
def read_organizations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    organizations = crud_org.get_organizations(db, skip=skip, limit=limit)
    return organizations


@router.get("/organizations/id/{id}", status_code=200, response_model=schema_org)
def read_organization(id: str, db: Session = Depends(get_db)):
    db_organization = crud_org.get_organization(db, id=id)
    if not db_organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    return db_organization

@router.get("/organizations/code/{code}", status_code=200, response_model=schema_org)
def read_organization_by_code(code: str, db: Session = Depends(get_db)):
    db_organization = crud_org.get_organization_by_code(db, code=code)
    if not db_organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    return db_organization
