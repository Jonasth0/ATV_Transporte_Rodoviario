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

class SaoGeraldoStrategy(ViagemStrategy):

    def identifica(self, payload: dict[str, Any]) -> bool:
        return (
            "codigoServico" in payload
            and "localEmbarque" in payload
            and "localDesembarque" in payload
            and "horarioPartida" in payload
            and "horarioChegada" in payload
        )

    def normaliza(
        self,
        payload: dict[str, Any],
    ) -> ViagemNormalizada:

        partida = converter_data(
            payload["horarioPartida"],
            "%Y-%m-%d %H:%M",
            campo="horarioPartida",
        )

        chegada = converter_data(
            payload["horarioChegada"],
            "%Y-%m-%d %H:%M",
            campo="horarioChegada",
        )

        duracao = converter_duracao(
            payload["tempoViagemMinutos"]
        )

        preco_valor = converter_preco_br(
            payload["precoPassagem"]
        )

        categoria = self._normalizar_categoria(
            payload["tipoAssento"]
        )

        assentos = converter_assentos(
            payload["vagasDisponiveis"]
        )

        validar_datas(partida, chegada)
        validar_duracao(partida, chegada, duracao)
        validar_preco(preco_valor)
        validar_assentos(assentos)

        validar_uf(payload["localEmbarque"]["uf"])
        validar_uf(payload["localDesembarque"]["uf"])
        validar_categoria(categoria)

        preco = Preco(
            valor=preco_valor,
            moeda=payload["moedaPagamento"],
        )

        return ViagemNormalizada(
            id_viagem=payload["codigoServico"],
            empresa=self.nome_empresa(),

            origem=Localidade(
                cidade=payload["localEmbarque"]["municipio"],
                uf=payload["localEmbarque"]["uf"],
            ),

            destino=Localidade(
                cidade=payload["localDesembarque"]["municipio"],
                uf=payload["localDesembarque"]["uf"],
            ),

            partida=partida,
            chegada=chegada,

            duracao_minutos=duracao,

            preco=preco,

            categoria=categoria,

            assentos_disponiveis=assentos,
        )

    def nome_empresa(self) -> str:
        return "São Geraldo"

    def _normalizar_categoria(
        self,
        valor: str,
    ) -> str:

        categorias = {
            "convencional": "convencional",
            "executivo": "executivo",
            "semi-leito": "semileito",
            "semileito": "semileito",
            "leito": "leito",
        }

        categoria = categorias.get(valor.lower())

        if categoria is None:
            raise ValueError("Categoria inválida.")

        return categoria
