from fastapi import HTTPException
from models.organization import Organization as model_org
from schemas import schemas
from utils.generic import MessageType
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .base import commit
from uuid import UUID


def create_organization(db: Session, organization: schemas.OrganizationSchema):
    """ Create an organization row for the table """
    db_org = db.query(model_org).filter(model_org.id == str(organization.id)).first()
    if db_org and db_org.code != organization.code: 
        raise HTTPException(status_code=400, detail="Input organization:'{}' already exists as:'{}' in the database".format(organization.code, db_org.code))
    elif db_org: raise HTTPException(status_code=400, detail="Input organization:'{}' already exists in the database".format(organization.code))
    
    db_org = model_org(id=str(organization.id), code=organization.code)
    try:
        commit(db, db_org)
    except IntegrityError: 
        raise HTTPException(status_code=400, detail="Input organization:'{}' already exists in the database".format(organization.code))
    return organization


def get_organization(db: Session, id: str):
    """ Get an organization from table with matching id """
    db_org = db.query(model_org).filter(model_org.id == id).first()
    if not db_org: 
        raise HTTPException(status_code=404, detail="Organization:'{}' does not exist in the database".format(id))
    return _populate_org_schema(id=db_org.id, code=db_org.code)


def get_organization_by_code(db: Session, code: str):
    """ Get an organization from table with matching code """
    db_org = db.query(model_org).filter(model_org.code == code).first()
    if not db_org: raise HTTPException(status_code=404, detail="Organization:'{}' does not exist in the database".format(code))
    return _populate_org_schema(id=db_org.id, code=db_org.code)


def get_organizations(db: Session, skip: int = 0, limit: int = 100):
    """ Fetch all organizations in the database"""
    db_orgs = db.query(model_org).offset(skip).limit(limit).all()
    if not db_orgs: raise HTTPException(status_code=404, detail="Organizations do not exist in the database")
    orgs = [_populate_org_schema(id=db_org.id, code=db_org.code) for db_org in db_orgs]
    return orgs


def update_organization(db: Session, organization: schemas):
    """ Update organization code for row in table that matches given id """
    db_org = db.query(model_org).filter(model_org.id == str(organization.id)).first()
    if not db_org:
        raise HTTPException(status_code=400, detail="Cannot update organization:'{}' is not in the database".format(organization.id))
    db_org.code = organization.code    
    db.commit()
    return organization


def remove_organization(db: Session, organization: schemas):
    """ Remove an organization from the table """
    db_org = db.query(model_org).get(str(organization.id))
    db.delete(db_org)
    db.commit()
    return organization


def _populate_org_schema(id:str, code:str):
    """ Helper function to populate org schema given organization model"""
    org = schemas.Organization(
            type=MessageType.org,
            id=UUID(id),
            code=code
        )
    return org