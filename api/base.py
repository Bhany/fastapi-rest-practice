from fastapi import APIRouter
from api.endpoints import shipment, organization, node


api_router = APIRouter()
api_router.include_router(shipment.router, tags=["shipment"])
api_router.include_router(organization.router, tags=["organization"])
api_router.include_router(node.router, tags=["node"])