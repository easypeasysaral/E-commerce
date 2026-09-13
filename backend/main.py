from fastapi import FastAPI, APIRouter
from routes import Products
import models
from databases import engine
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title= "This is the E-Commerce API")

@app.get("/")
async def root():
    return {
        'message' : "API is Working"
    }

app.include_router(Products.router)