from fastapi import APIRouter

router = APIRouter(
    prefix="/api/v1/viagens",
    tags=["Viagens"],
)

@router.post("/normalizar")
def normalizar_viagens():
    return {"mensagem": "Endpoint de normalização funcionando"}