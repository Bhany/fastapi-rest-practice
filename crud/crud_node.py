from sqlalchemy.sql.elements import conv
from fastapi import HTTPException
from models.node import Node as model_node
from schemas import node as schema_node
from utils.generic import WeightUnit, WeightConverter
from sqlalchemy.orm import Session
from sqlalchemy.sql import func


def get_nodes(db: Session, skip: int = 0, limit: int = 100):
    db_nodes = db.query(models.Node).offset(skip).limit(limit).all()

    nodes = []
    for db_node in db_nodes:
            
        total_weight = schema_node.TotalWeight(
            weight=db_node.weight,
            unit=db_node.original_unit)

        # add more node here in the future        
        node = schema_node.Node(totalWeight=total_weight)
        nodes.append(node)
    return nodes


# TODO: link with shipment, add to existing shipment
def _create_shipment_node(db: Session, node: schema_node.Node, referenceId: str):
    total_weight = node.totalWeight
    converted = WeightConverter.convert(total_weight.weight, total_weight.unit)

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


def _commit(db: Session, obj):
    db.add(obj)
    db.commit()
    db.refresh(obj)
