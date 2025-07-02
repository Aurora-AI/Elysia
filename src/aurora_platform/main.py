from fastapi import FastAPI
from .api.v1.router import api_v1_router

app = FastAPI(title="Aurora Platform")

app.include_router(api_v1_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to Aurora Platform"}
