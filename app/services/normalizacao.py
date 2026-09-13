from typing import Any

from app.domain.models.viagem import ViagensResponse
from app.domain.registry import StrategyRegistry


class NormalizacaoService:

    def __init__(self, registry: StrategyRegistry):
        self.registry = registry

    def normalizar(
        self,
        payloads: list[dict[str, Any]],
    ) -> ViagensResponse:

        viagens = []

        for payload in payloads:
            strategy = self.registry.identificar(payload)

            if strategy is None:
                raise ValueError(
                    "O formato do payload não corresponde "
                    "a nenhuma companhia suportada."
                )

            viagem = strategy.normaliza(payload)

            viagens.append(viagem)

        return ViagensResponse(
            total=len(viagens),
            viagens=viagens,
        )