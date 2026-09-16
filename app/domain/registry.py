from typing import Any

from app.domain.strategies.base import ViagemStrategy
from app.domain.strategies.gontijo import GontijoStrategy
from app.domain.strategies.progresso import ProgressoStrategy
from app.domain.strategies.rota import RotaStrategy
from app.domain.strategies.sao_geraldo import SaoGeraldoStrategy
from app.domain.strategies.sertao_bus import SertaoBusStrategy


class StrategyRegistry:

    def __init__(self):
        self._strategies: list[ViagemStrategy] = [
            ProgressoStrategy(),
            RotaStrategy(),
            GontijoStrategy(),
            SertaoBusStrategy(),
            SaoGeraldoStrategy(),
        ]

# PADRÃO STRATEGY - Testa cada adapter até um deles reconhecer o formato.

    def identificar(
        self,
        payload: dict[str, Any],
    ) -> ViagemStrategy | None: # Recebe um único payload, devolve um objeto strategy, ou "None" se nenhum servir.

        for strategy in self._strategies: # Lembra do Range? Esqueça, aqui já tem a lista pronta.
            if strategy.identifica(payload): # Recohece o payload. ( Executa um código de cada Strategy, polimorfismo meu filho ).
                return strategy

        return None