from sqlalchemy.orm import Session
from fastapi import HTTPException
from models import models
from schemas import schemas

def get_shipment(db: Session, referenceId: str):
    return db.query(models.Shipment).filter(models.Shipment.referenceId == referenceId).first()

def get_organization(db: Session, id: str):
    return db.query(models.Organization).filter(models.Organization.id == id).first()

def get_organization_by_code(db: Session, code: str):
    return db.query(models.Organization).filter(models.Organization.code == code).first()

def get_shipments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Shipment).offset(skip).limit(limit).all()

def get_organizations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Organization).offset(skip).limit(limit).all()

def get_nodes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Node).offset(skip).limit(limit).all()

def _commit(db: Session, obj):
    db.add(obj)
    db.commit()
    db.refresh(obj)

def create_shipment(db: Session, shipment: schemas.Shipment):
    current = db.query(models.Node).filter(models.Node.owner_id == shipment.referenceId).first()
    if not current:
        for pack in shipment.transportPacks:
            if 'nodes' in pack:
                for node in pack[1]:
                    if type(node) is schemas.Node:
                        create_shipment_node(db, node, shipment.referenceId)
                        current = db.query(models.Node).filter(models.Node.owner_id == shipment.referenceId).first()

    org_code_relations = []
    if shipment.organizations:
        for org_code in shipment.organizations:
            query_result = db.query(models.Organization).filter(models.Organization.code == org_code).first()
            if query_result: org_code_relations.append(query_result)
            else: raise HTTPException(status_code=400, detail="Invalid organization code, organization code: {} is not in the database".format(org_code))
        
    db_shipment = models.Shipment(
        referenceId = shipment.referenceId, 
        organizations = org_code_relations, 
        estimatedTimeArrival = shipment.estimatedTimeArrival,# if shipment.estimatedTimeArrival else None, 
        node_id = current.id)

    _commit(db, db_shipment)
    return shipment

def create_organization(db: Session, organization: schemas.Organization):
    db_organization = models.Organization(id=organization.id, code=organization.code)
    _commit(db, db_organization)
    return db_organization

def create_shipment_node(db: Session, node: schemas.Node, referenceId: str):
    total_weight = node.totalWeight
    if total_weight.unit == "OUNCES":
        converted = total_weight.weight * 0.0283495
        metric = False
    elif total_weight.unit == "KILOGRAMS":
        converted = total_weight.weight * 35.274
        metric = True
    else: 
        raise HTTPException(status_code=400, detail="Invalid weight unit: {}".format(total_weight.unit))

    db_node = models.Node(
        weight = total_weight.weight,
        original_unit = total_weight.unit,
        kg = total_weight.weight if metric else converted,
        lb = total_weight.weight if not metric else converted,
        owner_id = referenceId
    )
    _commit(db, db_node)
    return node
