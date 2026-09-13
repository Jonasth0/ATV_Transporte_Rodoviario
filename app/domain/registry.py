from typing import Any

from app.domain.strategies.base import ViagemStrategy
from app.domain.strategies.gontijo import GontijoStrategy
from app.domain.strategies.progresso import ProgressoStrategy
from app.domain.strategies.rota import RotaStrategy
from app.domain.strategies.sertao_bus import SertaoBusStrategy


class StrategyRegistry:

    def __init__(self):
        self._strategies: list[ViagemStrategy] = [
            ProgressoStrategy(),
            RotaStrategy(),
            GontijoStrategy(),
            SertaoBusStrategy(),
        ]

    def identificar(
        self,
        payload: dict[str, Any],
    ) -> ViagemStrategy | None:

        for strategy in self._strategies:
            if strategy.identifica(payload):
                return strategy

        return None