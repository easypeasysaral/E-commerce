from fastapi import FastAPI
from routes import Products, users
import models
from databases import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="This is the E-Commerce API")

@app.get("/")
async def root():
    return {'message': "API is Working"}

app.include_router(Products.router)
app.include_router(users.router)