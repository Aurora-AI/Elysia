from fastapi import FastAPI
from aurora_platform.api import kg_endpoints_pilares

app = FastAPI(title="Aurora KG API")

# Endpoints raiz


@app.get("/")
def root():
    return {"message": "Aurora KG API online"}


@app.get("/health")
def health():
    return {"status": "ok"}


# Registrar router dos pilares
app.include_router(kg_endpoints_pilares.router)
