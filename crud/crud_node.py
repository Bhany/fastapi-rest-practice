from fastapi import HTTPException
from models.node import Node as model_node
from schemas import schemas
from utils.generic import WeightUnit, WeightConverter
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from .base import commit


def create_shipment_node(db: Session, node: schemas.Node):
    """ Parse and convert weight and create entry in node table """
    total_weight = node.total_weight
    db_node = _node_with_conversion(total_weight.weight, total_weight.unit)
    commit(db, db_node)
    return db_node


def get_nodes(db: Session, skip: int=0, limit: int=100):
    """ Get all nodes in node table """
    db_nodes = db.query(model_node).offset(skip).limit(limit).all()
    if not db_nodes: raise HTTPException(status_code=404, detail="No nodes could be found")
    
    nodes = [
                schemas.Node(
                    total_weight = schemas.total_weight(
                        weight=db_node.weight,
                        unit=db_node.unit
                    )
                )
                for db_node in db_nodes
            ]
    return nodes


def update_node(db: Session, node: schemas, reference_id: str):
    """ 
    Update a single node row associated with shipment reference id 
    Note. Currently updates first node of query result (as is 1 to 1). 
    Must be updated if we want to specify 2/10/2022
    """
    db_node = db.query(model_node).filter(model_node.shipment_id == reference_id).first()
    if not db_node:
        raise HTTPException(status_code=404, detail="Cannot update node:'{}' is not in the database".format(node.id))
    total_weight = node.total_weight
    converted = WeightConverter.convert(total_weight.weight, total_weight.unit)
    
    db_node.weight = total_weight.weight
    db_node.unit = total_weight.unit
    db_node.kg = converted['kg']
    db_node.oz = converted['oz']
    db_node.lb = converted['lb']
    db.commit()
    return node


def remove_node(db: Session, node: schemas):
    """ Remove a node from node table """
    db_node = db.query(model_node).get(node.id)
    db.delete(db_node)
    db.commit()
    return node


def aggregate_node_weights(db: Session, unit=str):
    """ Scrape node table for weight values and its count according to given unit """
    if not WeightUnit.has_value(unit): 
        raise HTTPException(status_code=400, detail="Invalid weight unit:'{}'".format(unit))
    
    if unit == WeightUnit.oz: query_column = model_node.oz
    elif unit == WeightUnit.kg: query_column = model_node.kg
    elif unit == WeightUnit.lb: query_column = model_node.lb

    db_node = db.query(func.sum(query_column), func.count(query_column)).first()
    if not db_node: raise HTTPException(status_code=404, detail="Nodes are not found for aggregation")

    if db_node:
        weight = db_node[0] # func sum query result
        count = db_node[1] # func count query result

    return schemas.NodeAggregate(count=count, weight=weight, unit=unit)


def _node_with_conversion(weight:float, unit:str):
    """ Helper function to create node model with converted values """
    converted_weights = WeightConverter.convert(weight, unit)
    return model_node(weight=weight, unit=unit, kg=converted_weights['kg'], oz=converted_weights['oz'], lb=converted_weights['lb'])


""" TODO: if need for node to be created by itself arises
def create_node(db: Session, node: schemas.Node):
    total_weight = node.total_weight
    converted = WeightConverter.convert(total_weight.weight, total_weight.unit)

    db_node = model_node(
        weight = total_weight.weight,
        unit = total_weight.unit,
        kg = converted['kg'],
        oz = converted['oz'],
        lb = converted['lb'],
        shipment_id = None
    )
    _commit(db, db_node)
    return node
"""