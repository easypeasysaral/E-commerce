from fastapi import FastAPI

app = FastAPI(title= "E-commerce API")

@app.get("/")
async def root():
    return {
        'message' : "Backend is running"
    }