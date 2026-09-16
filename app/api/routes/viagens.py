from typing import Any

from fastapi import APIRouter

from app.domain.registry import StrategyRegistry
from app.services.normalizacao import NormalizacaoService


router = APIRouter(
    prefix="/api/v1/viagens",
    tags=["Viagens"],
)

# Só monta o registry e delega.
@router.post("/normalizar")
def normalizar_viagens(
    payloads: list[dict[str, Any]],
):
    registry = StrategyRegistry()
    service = NormalizacaoService(registry)

    return service.normalizar(payloads)