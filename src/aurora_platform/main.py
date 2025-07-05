from fastapi import FastAPI
from src.aurora_platform.routers import mentor_router # Adicione esta linha

app = FastAPI(title="Aurora Core")

@app.get("/")
def read_root():
    return {"message": "Bem-vindo ao Aurora Core. O Cérebro está despertando."}

app.include_router(mentor_router.router, prefix="/mentor/sales", tags=["Sales Mentor"]) # Adicione esta linha