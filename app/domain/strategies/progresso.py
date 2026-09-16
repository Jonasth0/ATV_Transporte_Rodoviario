from typing import Any

from app.domain.models.viagem import (
    Localidade,
    Preco,
    ViagemNormalizada,
)
from app.domain.strategies.base import ViagemStrategy
from app.domain.utils.conversores import (
    converter_assentos,
    converter_data,
    converter_duracao,
    converter_preco_br,
)
from app.domain.utils.validadores import (
    validar_assentos,
    validar_categoria,
    validar_datas,
    validar_duracao,
    validar_preco,
    validar_uf,
)


class ProgressoStrategy(ViagemStrategy):

# Cada empresa manda um JSON com nomes de campos diferentes.
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

        partida = converter_data(
            payload["dataHoraSaida"],
            "%d/%m/%Y %H:%M",
            "partida",
        )

        chegada = converter_data(
            payload["dataHoraChegada"],
            "%d/%m/%Y %H:%M",
            "chegada",
        )

        duracao = converter_duracao(
            payload["tempoEstimado"]
        )

        preco_valor = converter_preco_br(
            payload["valorPassagem"]
        )

        categoria = self._normalizar_categoria(
            payload["tipoServico"]
        )

        assentos = converter_assentos(
            payload["assentosDisponiveis"]
        )

        validar_datas(partida, chegada)
        validar_duracao(partida, chegada, duracao)
        validar_preco(preco_valor)
        validar_assentos(assentos)

        validar_uf(payload["ufOrigem"])
        validar_uf(payload["ufDestino"])
        validar_categoria(categoria)

        preco = Preco(
            valor=preco_valor,
            moeda="BRL",
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