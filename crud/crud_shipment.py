from fastapi import HTTPException
from models.shipment import Shipment as model_ship
from models.organization import Organization as model_org
from models.node import Node as model_node
from schemas import shipment as schema_ship
from schemas import node as schema_node

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
            db_node = db.query(model_ship).filter(model_ship.id == db_shipment.node_id).first()
            
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


def _commit(db: Session, obj):
    db.add(obj)
    db.commit()
    db.refresh(obj)

def create_shipment(db: Session, shipment: schema_ship.Shipment):
    current = db.query(model_node).filter(model_node.owner_id == shipment.referenceId).first()
    if not current:
        for pack in shipment.transportPacks:
            if 'nodes' in pack:
                for node in pack[1]:
                    if type(node) is schema_node.Node:
                        _create_shipment_node(db, node, shipment.referenceId)
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

# TODO: link with shipment, add to existing shipment
def _create_shipment_node(db: Session, node: schema_node.Node, referenceId: str):
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

    db_node = model_node(
        weight = total_weight.weight,
        original_unit = total_weight.unit,
        kg = kilograms,
        oz = ounces,
        lb = pounds,
        owner_id = referenceId
    )
    _commit(db, db_node)
    return node
