from fastapi import FastAPI, APIRouter
from routes import Products
app = FastAPI(title= "This is the E-Commerce API")

@app.get("/")
async def Root():
    return {
        'message' : "API is Working"
    }

app.include_router(Products.router)