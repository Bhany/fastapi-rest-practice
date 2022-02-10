from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from crud import crud_organization as crud_org
from schemas import schemas
from api.deps import get_db

router = APIRouter()

@router.post("/organization/", status_code=201, response_model=schemas.Organization)
def create_organization(organization: schemas.Organization, db: Session = Depends(get_db)):
    return crud_org.create_organization(db=db, organization=organization)


@router.get("/organizations/", status_code=200, response_model=List[schemas.Organization])
def read_organizations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_org.get_organizations(db, skip=skip, limit=limit)


@router.get("/organizations/id/{id}", status_code=200, response_model=schemas.Organization)
def read_organization(id: str, db: Session = Depends(get_db)):
    return crud_org.get_organization(db, id=id)


@router.get("/organizations/code/{code}", status_code=200, response_model=schemas.Organization)
def read_organization_by_code(code: str, db: Session = Depends(get_db)):
    return crud_org.get_organization_by_code(db, code=code)
