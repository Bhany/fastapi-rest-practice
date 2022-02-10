from fastapi import HTTPException
from models.shipment import Shipment as model_ship
from models.organization import Organization as model_org
from models.node import Node as model_node
from schemas import schemas
from .crud_node import create_shipment_node
from sqlalchemy.orm import Session, joinedload
from utils.generic import MessageType
from .base import commit


def create_shipment(db: Session, shipment: schemas.ShipmentSchema):
    """ Create shipment row by mapping schema into model shipment then insert """
    db_ship = db.query(model_ship).filter(model_ship.reference_id == shipment.reference_id).first()
    if db_ship: 
        raise HTTPException(status_code=404, detail="Shipment with reference id:'{}' already exist in the database".format(shipment.reference_id))

    transport_packs = [create_shipment_node(db, node) for node in shipment.transport_packs.nodes]
    
    org_code_relations = []
    for org_code in shipment.organizations:
        query_result = db.query(model_org).filter(model_org.code == org_code).first()
        if query_result: org_code_relations.append(query_result)
        else: raise HTTPException(status_code=400, detail="Invalid organization code, organization code:'{}' is not in the database".format(org_code))

    db_shipment = model_ship(
            reference_id = shipment.reference_id, 
            organizations = org_code_relations, 
            estimated_time_arrival = shipment.estimated_time_arrival,
            transport_packs = transport_packs
        )

    commit(db, db_shipment)
    return shipment


def get_shipment(db: Session, reference_id: str):
    """ Get shipment row matching reference id return as schema """
    db_ship = db.query(model_ship).filter(model_ship.reference_id == reference_id).options(joinedload(model_ship.organizations)).first()
    if not db_ship: raise HTTPException(status_code=404, detail="Shipment does not exist in the database")

    shipment = None

    org_codes = [orgs.code for orgs in db_ship.organizations]        

    eta = db_ship.estimated_time_arrival if db_ship.estimated_time_arrival else None
    
    nodes = [
            schemas.Node(
                total_weight=schemas.total_weight(
                    weight=db_node.weight, 
                    unit=db_node.unit
                    )
                )
            for db_node in db_ship.transport_packs
        ]
    transportPack = schemas.TransportPacks(nodes=nodes)
    
    shipment = schemas.ShipmentSchema(
        type=MessageType.ship,
        reference_id=db_ship.reference_id,
        organizations=org_codes,
        estimated_time_arrival=eta,
        transport_packs=transportPack,
    )

    return shipment


def get_shipments(db: Session, skip: int = 0, limit: int = 100):
    """ Get all shipments """
    db_ships = db.query(model_ship).offset(skip).limit(limit).all()
    shipments = []

    for db_ship in db_ships:
        org_codes = [org.code for org in db_ship.organizations]

        eta = db_ship.estimated_time_arrival if db_ship.estimated_time_arrival else None
        
        nodes = [
            schemas.Node(
                total_weight=schemas.total_weight(
                    weight=db_node.weight, 
                    unit=db_node.unit
                    )
                )
            for db_node in db_ship.transport_packs
        ]
        transportPack = schemas.TransportPacks(nodes=nodes)
        
        shipment = schemas.ShipmentSchema(
            type=MessageType.ship,
            reference_id=db_ship.reference_id,
            organizations=org_codes,
            estimated_time_arrival=eta,
            transport_packs=transportPack,
        )

        shipments.append(shipment)

    return shipments


def update_shipment(db: Session, shipment: schemas.Shipment):
    """ Update shipment row if exist """
    db_ship = db.query(model_node).filter(model_node.shipment_id == shipment.reference_id).first()
    if not db_ship:
        raise HTTPException(status_code=404, detail="Cannot update shipment:'{}' is not in the database".format(shipment.reference_id))

    # currently update a single related node; should do so on the node crud
    """
    db_node = db.query(model_node).filter(model_node.shipment_id == shipment.reference_id).one()
    for pack in shipment.transport_packs:
        for node in pack.nodes:
            if db_node:
                update_node(db, node, shipment.reference_id)
                current = db.query(model_node).filter(model_node.shipment_id == shipment.reference_id).one()
                current = current.id
    """
    org_code_relations = []
    for org_code in shipment.organizations:
        query_result = db.query(model_org).filter(model_org.code == org_code).first()
        if query_result: org_code_relations.append(query_result)
        else: raise HTTPException(status_code=400, detail="Invalid organization code, organization code:'{}' is not in the database".format(org_code))
        
    db_ship.reference_id = shipment.reference_id
    db_ship.organizations = org_code_relations
    db_ship.estimated_time_arrival = shipment.estimated_time_arrival
    db.commit()
    return shipment


def remove( db: Session, shipment: schemas.Shipment):
    """ Remove shipment and its associated nodes """
    db_ship = db.query(model_ship).get(shipment.reference_id)
    db.delete(db_ship)

    db_node = db.query(model_node).get(model_node.shipment_id == shipment.reference_id)
    db.delete(db_node)
    db.commit()
    return shipment