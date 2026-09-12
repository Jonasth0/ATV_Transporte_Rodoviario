from fastapi import FastAPI
from app.api.routes import viagens

app = FastAPI(
    title= "API de Normalização de Viagens",
    descripition= "API para normalização de dados de viagens de diferentes companhias.",
    version= "1.0.0",
)

app.include_router(viagens.router)