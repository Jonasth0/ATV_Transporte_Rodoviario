from datetime import datetime
from decimal import Decimal
from typing import Any

from app.domain.models.viagem import (
    Localidade,
    Preco,
    ViagemNormalizada,
)
from app.domain.strategies.base import ViagemStrategy


class ProgressoStrategy(ViagemStrategy):

    def identifica(self, payload: dict[str, Any]) -> bool:
        return (
            "codigoViagem" in payload
            and "cidadeOrigem" in payload
            and "ufOrigem" in payload
            and "cidadeDestino" in payload
            and "ufDestino" in payload
            and "dataHoraSaida" in payload
            and "dataHoraChegada" in payload
        )

    def normaliza(
        self,
        payload: dict[str, Any],
    ) -> ViagemNormalizada:

        partida = self._converter_data(
            payload["dataHoraSaida"]
        )

        chegada = self._converter_data(
            payload["dataHoraChegada"]
        )

        duracao = self._converter_duracao(
            payload["tempoEstimado"]
        )

        preco = self._converter_preco(
            payload["valorPassagem"]
        )

        categoria = self._normalizar_categoria(
            payload["tipoServico"]
        )

        assentos = self._converter_assentos(
            payload["assentosDisponiveis"]
        )

        return ViagemNormalizada(
            id_viagem=payload["codigoViagem"],
            empresa=self.nome_empresa(),
            origem=Localidade(
                cidade=payload["cidadeOrigem"],
                uf=payload["ufOrigem"],
            ),
            destino=Localidade(
                cidade=payload["cidadeDestino"],
                uf=payload["ufDestino"],
            ),
            partida=partida,
            chegada=chegada,
            duracao_minutos=duracao,
            preco=preco,
            categoria=categoria,
            assentos_disponiveis=assentos,
        )

    def nome_empresa(self) -> str:
        return "Auto Viação Progresso"

    def _converter_data(self, valor: str) -> datetime:
        return datetime.strptime(
            valor,
            "%d/%m/%Y %H:%M",
        )

    def _converter_duracao(self, valor: str) -> int:
        horas, minutos = valor.split(":")
        return int(horas) * 60 + int(minutos)

    def _converter_preco(self, valor: str) -> Preco:
        valor_decimal = Decimal(
            valor.replace(".", "").replace(",", ".")
        )

        return Preco(
            valor=valor_decimal,
            moeda="BRL",
        )

    def _normalizar_categoria(self, valor: str) -> str:
        categorias = {
            "CONVENCIONAL": "convencional",
            "EXECUTIVO": "executivo",
            "SEMILEITO": "semileito",
            "LEITO": "leito",
        }

        categoria = categorias.get(valor.upper())

        if categoria is None:
            raise ValueError("Categoria inválida.")

        return categoria

    def _converter_assentos(self, valor: str) -> int:
        return int(valor)