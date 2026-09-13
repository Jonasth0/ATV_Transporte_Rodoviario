from typing import Any

from app.domain.models.viagem import ViagensResponse
from app.domain.registry import StrategyRegistry
from app.exceptions.viagem import ViagemValidationError


class NormalizacaoService:

    def __init__(self, registry: StrategyRegistry):
        self.registry = registry

    def normalizar(
        self,
        payloads: list[dict[str, Any]],
    ) -> ViagensResponse:

        viagens = []

        for indice, payload in enumerate(payloads):

            strategy = self.registry.identificar(payload)

            if strategy is None:
                raise ViagemValidationError(
                    campo=None,
                    mensagem=(
                        "O formato do payload não corresponde "
                        "a nenhuma companhia suportada."
                    ),
                    indice=indice,
                    empresa_identificada=None,
                )

            try:
                viagem = strategy.normaliza(payload)

            except ViagemValidationError as erro:
                raise ViagemValidationError(
                    campo=erro.campo,
                    mensagem=erro.mensagem,
                    indice=indice,
                    empresa_identificada=strategy.nome_empresa(),
                ) from erro

            except KeyError as erro:
                raise ViagemValidationError(
                    campo=str(erro.args[0]),
                    mensagem="Campo obrigatório não informado.",
                    indice=indice,
                    empresa_identificada=strategy.nome_empresa(),
                ) from erro

            except (ValueError, TypeError) as erro:
                raise ViagemValidationError(
                    campo=None,
                    mensagem=str(erro),
                    indice=indice,
                    empresa_identificada=strategy.nome_empresa(),
                ) from erro

            viagens.append(viagem)

        return ViagensResponse(
            total=len(viagens),
            viagens=viagens,
        )