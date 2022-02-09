from fastapi import HTTPException
from models.organization import Organization as model_org
from schemas.organization import Organization as schema_org
from sqlalchemy.orm import Session

import uuid


def create_organization(db: Session, organization: schema_org):
    exist = get_organization(db, str(organization.id))
    if exist: 
        update_organization(db, organization)
        return organization
    db_organization = model_org(id=str(organization.id), code=organization.code)
    _commit(db, db_organization)
    return organization


def get_organization(db: Session, id: str):
    db_org = db.query(model_org).filter(model_org.id == id).first()
    org = None
    if db_org:
        org = schema_org(
            type="ORGANIZATION",
            id=uuid.UUID(db_org.id),
            code=db_org.code
        )
    return org


def get_organization_by_code(db: Session, code: str):
    db_organization = db.query(model_org).filter(model_org.code == code).first()
    org = schema_org(
            type="ORGANIZATION",
            id=uuid.UUID(db_organization.id),
            code=db_organization.code
        )
    return org


def get_organizations(db: Session, skip: int = 0, limit: int = 100):
    db_orgs = db.query(model_org).offset(skip).limit(limit).all()
    orgs = []
    for db_org in db_orgs:
        org = schema_org(
            type="ORGANIZATION",
            id=uuid.UUID(db_org.id),
            code=db_org.code
        )
        orgs.append(org)
    return orgs


def remove_organization(db: Session, organization: schema_org):
    obj = db.query(model_org).get(str(organization.id))
    db.delete(obj)
    db.commit()
    return organization


def update_organization(db: Session, organization: schema_org):
    db_org = db.query(model_org).filter(model_org.id == str(organization.id)).first()
    if not db_org:
        raise HTTPException(status_code=400, detail="Cannot update organization: {} is not in the database".format(organization.id))
    db_org.code = organization.code    
    db.commit()
    return organization


def _commit(db: Session, obj):
    db.add(obj)
    db.commit()
    db.refresh(obj)
