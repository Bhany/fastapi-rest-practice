from fastapi import HTTPException
from models import models
from schemas import schemas
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

import uuid

def get_shipment(db: Session, referenceId: str):
    db_shipment = db.query(models.Shipment).filter(models.Shipment.referenceId == referenceId).first()
    shipment = None
    
    if db_shipment:
        org_codes = []
        for org in db_shipment.organizations:
            org_codes.append(org.code)
        
        eta = None
        if db_shipment.estimatedTimeArrival:
            eta = db_shipment.estimatedTimeArrival
        
        nodes = []
        if db_shipment.node_id:
            db_nodes = db.query(models.Node).filter(models.Node.id == db_shipment.node_id)
            
            for db_node in db_nodes:
                total_weight = schemas.TotalWeight(
                    weight=db_node.weight,
                    unit=db_node.original_unit)

                # add more node here in the future        
                node = schemas.Node(totalWeight=total_weight)
                nodes.append(node)
            
        transportPack = schemas.TransportPacks(nodes=nodes)
        
        shipment = schemas.Shipment(
            type="SHIPMENT",
            referenceId=db_shipment.referenceId,
            organizations=org_codes,
            estimatedTimeArrival=eta,
            transportPacks=transportPack,
        )

    return shipment


def get_organization(db: Session, id: str):
    db_org = db.query(models.Organization).filter(models.Organization.id == str(id)).first()
    org = None
    if db_org:
        org = schemas.Organization(
            type="ORGANIZATION",
            id=uuid.UUID(db_org.id),
            code=db_org.code
        )
    return org


def get_organization_by_code(db: Session, code: str):
    db_organization = db.query(models.Organization).filter(models.Organization.code == code).first()
    org = schemas.Organization(
            type="ORGANIZATION",
            id=uuid.UUID(db_organization.id),
            code=db_organization.code
        )
    return org

def get_shipments(db: Session, skip: int = 0, limit: int = 100):
    db_shipments = db.query(models.Shipment).offset(skip).limit(limit).all()
    shipments = []

    for db_shipment in db_shipments:
        org_codes = []
        for org in db_shipment.organizations:
            org_codes.append(org.code)
        
        eta = None
        if db_shipment.estimatedTimeArrival:
            eta = db_shipment.estimatedTimeArrival
        
        nodes = []
        if db_shipment.node_id:
            db_node = db.query(models.Node).filter(models.Node.id == db_shipment.node_id).first()
            
            total_weight = schemas.TotalWeight(
                weight=db_node.weight,
                unit=db_node.original_unit)

            # add more node here in the future        
            node = schemas.Node(totalWeight=total_weight)
            nodes.append(node)
            
        transportPack = schemas.TransportPacks(nodes=nodes)
        
        shipment = schemas.Shipment(
            type="SHIPMENT",
            referenceId=db_shipment.referenceId,
            organizations=org_codes,
            estimatedTimeArrival=eta,
            transportPacks=transportPack,
        )

        shipments.append(shipment)
    return shipments


def get_organizations(db: Session, skip: int = 0, limit: int = 100):
    db_orgs = db.query(models.Organization).offset(skip).limit(limit).all()
    orgs = []
    for db_org in db_orgs:
        org = schemas.Organization(
            type="ORGANIZATION",
            id=uuid.UUID(db_org.id),
            code=db_org.code
        )
        orgs.append(org)
    return orgs

def get_nodes(db: Session, skip: int = 0, limit: int = 100):
    db_nodes = db.query(models.Node).offset(skip).limit(limit).all()

    nodes = []
    for db_node in db_nodes:
            
        total_weight = schemas.TotalWeight(
            weight=db_node.weight,
            unit=db_node.original_unit)

        # add more node here in the future        
        node = schemas.Node(totalWeight=total_weight)
        nodes.append(node)
    return nodes


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
                        _create_shipment_node(db, node, shipment.referenceId)
                        current = db.query(models.Node).filter(models.Node.owner_id == shipment.referenceId).first()
                        current = current.id


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
        node_id = current)

    _commit(db, db_shipment)
    return shipment

def create_organization(db: Session, organization: schemas.Organization):
    db_organization = models.Organization(id=str(organization.id), code=organization.code)
    _commit(db, db_organization)
    return organization

# TODO: link with shipment, add to existing shipment
def _create_shipment_node(db: Session, node: schemas.Node, referenceId: str):
    total_weight = node.totalWeight
    if total_weight.unit == "OUNCES":
        kilograms = total_weight.weight * 0.0283495
        pounds =  total_weight.weight * 0.0625
        ounces = total_weight.weight
    elif total_weight.unit == "KILOGRAMS":
        kilograms = total_weight.weight
        pounds = total_weight.weight * 2.20462
        ounces = total_weight.weight * 35.274
    elif total_weight.unit == "POUNDS":
        kilograms = total_weight.weight * 0.453592
        pounds = total_weight.weight 
        ounces = total_weight.weight * 16
    else: 
        raise HTTPException(status_code=400, detail="Invalid weight unit: {}".format(total_weight.unit))

    db_node = models.Node(
        weight = total_weight.weight,
        original_unit = total_weight.unit,
        kg = kilograms,
        oz = ounces,
        lb = pounds,
        owner_id = referenceId
    )
    _commit(db, db_node)
    return node

def aggregate_node_weights(db: Session, unit=str):
    w = schemas.WeightUnit
    if unit != w.oz and unit != w.kg and unit != w.lb: 
        raise HTTPException(status_code=400, detail="Invalid weight unit: {}; allowed input: 'OUNCES', KILOGRAMS, and 'POUNDS'".format(unit))
    if unit == w.oz: model = models.Node.oz
    elif unit == w.kg: model = models.Node.kg
    elif unit == w.lb: model = models.Node.lb

    result = db.query(func.sum(model), func.count(model)).first()
    
    if result:
        weight = result[0]
        count = result[1]

    return schemas.NodeAggregate(count=count, weight=weight, unit=unit)