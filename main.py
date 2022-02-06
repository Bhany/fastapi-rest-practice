from typing import Optional
from fastapi import FastAPI, Query
import schemas.shipment as s

app = FastAPI(title="TODO TITLE", openapi_url="/openapi.json")

# TODO: create landing page
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get('/{query_type}/{id}')
async def read_item(query_type: s.QueryGetType, id: Optional[str]=Query(None, )): # str data validation
    return {s.QueryGetType(query_type): id}

@app.post('/shipment/')
async def create_item(item: s.Shipment): 
    return "ok"

@app.put('/organization/')
async def create_item(item: s.Organization):
    return item
