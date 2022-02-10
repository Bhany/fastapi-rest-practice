
from fastapi import FastAPI, APIRouter
from api.base import api_router

root_router = APIRouter()
app = FastAPI(title="shipment API", openapi_url="/api/openapi.json")

@root_router.get("/") 
def root(): return {"hello": "world"}

app.include_router(api_router)
app.include_router(root_router)
