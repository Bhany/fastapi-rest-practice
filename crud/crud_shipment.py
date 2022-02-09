from sqlalchemy import schema
from fastapi import HTTPException
from models.shipment import Shipment as model_ship
from models.organization import Organization as model_org
from models.node import Node as model_node
from schemas import shipment as schema_ship
from schemas import node as schema_node
from .crud_node import create_shipment_node, update_node
from sqlalchemy.orm import Session


def get_shipment(db: Session, referenceId: str):
    db_shipment = db.query(model_ship).filter(model_ship.referenceId == referenceId).first()
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
            db_nodes = db.query(model_node).filter(model_node.id == db_shipment.node_id)
            
            for db_node in db_nodes:
                total_weight = schema_node.TotalWeight(
                    weight=db_node.weight,
                    unit=db_node.original_unit)

                # add more node here in the future        
                node = schema_node.Node(totalWeight=total_weight)
                nodes.append(node)
            
        transportPack = schema_ship.TransportPacks(nodes=nodes)
        
        shipment = schema_ship.Shipment(
            type="SHIPMENT",
            referenceId=db_shipment.referenceId,
            organizations=org_codes,
            estimatedTimeArrival=eta,
            transportPacks=transportPack,
        )

    return shipment


def get_shipments(db: Session, skip: int = 0, limit: int = 100):
    db_shipments = db.query(model_ship).offset(skip).limit(limit).all()
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
            db_node = db.query(model_node).filter(model_node.id == db_shipment.node_id).first()
            
            total_weight = schema_node.TotalWeight(
                weight=db_node.weight,
                unit=db_node.original_unit)

            # add more node here in the future        
            node = schema_node.Node(totalWeight=total_weight)
            nodes.append(node)
            
        transportPack = schema_ship.TransportPacks(nodes=nodes)
        
        shipment = schema_ship.Shipment(
            type="SHIPMENT",
            referenceId=db_shipment.referenceId,
            organizations=org_codes,
            estimatedTimeArrival=eta,
            transportPacks=transportPack,
        )

        shipments.append(shipment)
    return shipments


def create_shipment(db: Session, shipment: schema_ship.Shipment):
    exist = db.query(model_ship).filter(model_ship.referenceId == shipment.referenceId).first()
    if exist: update_shipment(db, shipment)

    db_node = db.query(model_node).filter(model_node.owner_id == shipment.referenceId).first()
    current = None
    for pack in shipment.transportPacks:
        if 'nodes' in pack:
            for node in pack[1]:
                if type(node) is schema_node.Node:
                    if db_node:
                        update_node(db, node, shipment.referenceId)
                    else:
                        create_shipment_node(db, node, shipment.referenceId)
                    current = db.query(model_node).filter(model_node.owner_id == shipment.referenceId).first()
                    current = current.id

    org_code_relations = []
    if shipment.organizations:
        for org_code in shipment.organizations:
            query_result = db.query(model_org).filter(model_org.code == org_code).first()
            if query_result: org_code_relations.append(query_result)
            else: raise HTTPException(status_code=400, detail="Invalid organization code, organization code: {} is not in the database".format(org_code))
        
    db_shipment = model_ship(
        referenceId = shipment.referenceId, 
        organizations = org_code_relations, 
        estimatedTimeArrival = shipment.estimatedTimeArrival,# if shipment.estimatedTimeArrival else None, 
        node_id = current)

    _commit(db, db_shipment)
    return shipment


def remove(self, db: Session, shipment: schema_ship.Shipment):
    obj = db.query(model_ship).get(shipment.referenceId)
    db.delete(obj)
    db.commit()

    obj = db.query(model_node).get(model_node.owner_id == shipment.referenceId)
    if obj:
        db.delete(obj)
        db.commit()
    return shipment


def update_shipment(db: Session, shipment: schema_ship.Shipment):
    db_shipment = db.query(model_node).filter(model_node.owner_id == shipment.referenceId).first()
    if not db_shipment:
        raise HTTPException(status_code=400, detail="Cannot update shipment: {} is not in the database".format(shipment.referenceId))

    db_node = db.query(model_node).filter(model_node.owner_id == shipment.referenceId).first()
    for pack in shipment.transportPacks:
        if 'nodes' in pack:
            for node in pack[1]:
                if type(node) is schema_node.Node:
                    if db_node:
                        update_node(db, node, shipment.referenceId)
                    else:
                        create_shipment_node(db, node, shipment.referenceId)
                    current = db.query(model_node).filter(model_node.owner_id == shipment.referenceId).first()
                    current = current.id

    org_code_relations = []
    if shipment.organizations:
        for org_code in shipment.organizations:
            query_result = db.query(model_org).filter(model_org.code == org_code).first()
            if query_result: org_code_relations.append(query_result)
            else: raise HTTPException(status_code=400, detail="Invalid organization code, organization code: {} is not in the database".format(org_code))
        
    db_shipment.referenceId = shipment.referenceId
    db_shipment.organizations = org_code_relations
    db_shipment.estimatedTimeArrival = shipment.estimatedTimeArrival
    db_shipment.node_id = current
    db.commit()
    return shipment


def _commit(db: Session, obj):
    db.add(obj)
    db.commit()
    db.refresh(obj)
