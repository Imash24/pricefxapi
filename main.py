from fastapi import APIRouter, FastAPI, HTTPException, Query
from fastapi.responses import RedirectResponse
import httpx
from base64 import b64encode
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
app = FastAPI()

app.mount("/static", StaticFiles(directory="frontend"), name="static")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




PARTITION_NAME = "demofx_bprasath"
USERNAME = "June-Mahesh"
PASSWORD = "start123"
BASE_URL = "https://demo-eu.demo1.pricefx.com/pricefx"  

encoded_credentials = b64encode(f"{PARTITION_NAME}/{USERNAME}:{PASSWORD}".encode()).decode()

@app.post("/search-product/")
async def search_product(q: str = Query(..., description="Enter the product SKU or label to search")):
    
    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/json"
    }

    
    data = {
        "data": {
            "q": q
        }
    }

    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{BASE_URL}/{PARTITION_NAME}/productmanager.quicksearch", json=data, headers=headers)

        
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
    
    
# Redirect the base URL to /static/index.html
@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/static/index.html")
