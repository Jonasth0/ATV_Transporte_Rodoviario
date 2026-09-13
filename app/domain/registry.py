from typing import Any

from app.domain.strategies.base import ViagemStrategy
from app.domain.strategies.progresso import ProgressoStrategy
from app.domain.strategies.rota import RotaStrategy


class StrategyRegistry:

    def __init__(self):
        self._strategies: list[ViagemStrategy] = [
            ProgressoStrategy(),
            RotaStrategy(),
        ]

    def identificar(
        self,
        payload: dict[str, Any],
    ) -> ViagemStrategy | None:

        for strategy in self._strategies:
            if strategy.identifica(payload):
                return strategy

        return None