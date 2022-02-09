from sqlalchemy.sql.elements import conv
from fastapi import HTTPException
from models.node import Node as model_node
from schemas import node as schema_node
from utils.generic import WeightUnit, WeightConverter
from sqlalchemy.orm import Session
from sqlalchemy.sql import func


def get_nodes(db: Session, skip: int = 0, limit: int = 100):
    db_nodes = db.query(model_node).offset(skip).limit(limit).all()

    nodes = []
    for db_node in db_nodes:
            
        total_weight = schema_node.TotalWeight(
            weight=db_node.weight,
            unit=db_node.original_unit)

        # add more node here in the future        
        node = schema_node.Node(totalWeight=total_weight)
        nodes.append(node)
    return nodes


def create_shipment_node(db: Session, node: schema_node.Node, referenceId: str):
    total_weight = node.totalWeight
    c = WeightConverter()
    converted = c.convert(total_weight.weight, total_weight.unit)

    db_node = model_node(
        weight = total_weight.weight,
        original_unit = total_weight.unit,
        kg = converted['kg'],
        oz = converted['oz'],
        lb = converted['lb'],
        owner_id = referenceId
    )
    _commit(db, db_node)
    return node

def aggregate_node_weights(db: Session, unit=str):
    w = WeightUnit
    if unit != w.oz and unit != w.kg and unit != w.lb: 
        raise HTTPException(status_code=400, detail="Invalid weight unit: {}; allowed input: 'OUNCES', KILOGRAMS, and 'POUNDS'".format(unit))
    if unit == w.oz: model = model_node.oz
    elif unit == w.kg: model = model_node.kg
    elif unit == w.lb: model = model_node.lb

    result = db.query(func.sum(model), func.count(model)).first()
    
    if result:
        weight = result[0]
        count = result[1]

    return schema_node.NodeAggregate(count=count, weight=weight, unit=unit)


def remove_node(self, db: Session, node: schema_node):
    obj = db.query(model_node).get(node.id)
    db.delete(obj)
    db.commit()
    return node


def update_node(db: Session, node: schema_node, referenceId: str):
    db_node = db.query(model_node).filter(model_node.owner_id == referenceId).first()
    if not db_node:
        raise HTTPException(status_code=400, detail="Cannot update node: {} is not in the database".format(node.id))
    total_weight = node.totalWeight
    c = WeightConverter()
    converted = c.convert(total_weight.weight, total_weight.unit)
    
    db_node.weight = total_weight.weight
    db_node.original_unit = total_weight.unit
    db_node.kg = converted['kg']
    db_node.oz = converted['oz']
    db_node.lb = converted['lb']
    db_node.owner_id = referenceId
    return node


def _commit(db: Session, obj):
    db.add(obj)
    db.commit()
    db.refresh(obj)


""" TODO: if need for node to be created by itself arises
def create_node(db: Session, node: schema_node.Node):
    total_weight = node.totalWeight
    converted = WeightConverter.convert(total_weight.weight, total_weight.unit)

    db_node = model_node(
        weight = total_weight.weight,
        original_unit = total_weight.unit,
        kg = converted['kg'],
        oz = converted['oz'],
        lb = converted['lb'],
        owner_id = None
    )
    _commit(db, db_node)
    return node
"""