
from fastapi import Depends, FastAPI, APIRouter
from sqlalchemy.orm import Session
from typing import Union

from crud.crud_organization import create_organization
from crud.crud_shipment import create_shipment
from schemas.shipment import Shipment as schema_ship
from schemas.organization import Organization as schema_org
from api.deps import get_db
from api.base import api_router

root_router = APIRouter()
app = FastAPI(title="shipment API", openapi_url="/api/openapi.json")

@root_router.post("/message/", response_model=Union[schema_ship, schema_org]) 
def receive_message(message: Union[schema_ship, schema_org], db: Session = Depends(get_db)):
    message_type = type(message)
    if message_type == schema_org:
        create_organization(db, message) #TODO call one create, pass model
    elif message_type == schema_ship:
        create_shipment(db, message)
    return message

app.include_router(api_router)
app.include_router(root_router)
