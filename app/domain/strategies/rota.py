from datetime import datetime
from decimal import Decimal
from typing import Any

from app.domain.models.viagem import (
    Localidade,
    Preco,
    ViagemNormalizada,
)
from app.domain.strategies.base import ViagemStrategy


class RotaStrategy(ViagemStrategy):

    def identifica(self, payload: dict[str, Any]) -> bool:
        return (
            "trip_id" in payload
            and "origem" in payload
            and "destino" in payload
            and "partida_em" in payload
            and "chegada_em" in payload
        )

    def normaliza(
        self,
        payload: dict[str, Any],
    ) -> ViagemNormalizada:

        partida = datetime.fromisoformat(
            payload["partida_em"]
        )

        chegada = datetime.fromisoformat(
            payload["chegada_em"]
        )

        preco = Decimal(payload["tarifa_centavos"]) / 100

        return ViagemNormalizada(
            id_viagem=payload["trip_id"],
            empresa=self.nome_empresa(),

            origem=Localidade(
                cidade=payload["origem"]["municipio"],
                uf=payload["origem"]["estado"],
            ),

            destino=Localidade(
                cidade=payload["destino"]["municipio"],
                uf=payload["destino"]["estado"],
            ),

            partida=partida,
            chegada=chegada,

            duracao_minutos=payload["duracao_minutos"],

            preco=Preco(
                valor=preco,
                moeda=payload["moeda"],
            ),

            categoria=self._normalizar_categoria(
                payload["classe"]
            ),

            assentos_disponiveis=payload["vagas"],
        )

    def nome_empresa(self) -> str:
        return "Rota Transportes"

    def _normalizar_categoria(self, valor: str) -> str:
        categorias = {
            "convencional": "convencional",
            "executivo": "executivo",
            "semileito": "semileito",
            "leito": "leito",
        }

        categoria = categorias.get(valor.lower())

        if categoria is None:
            raise ValueError("Categoria inválida.")

        return categoria