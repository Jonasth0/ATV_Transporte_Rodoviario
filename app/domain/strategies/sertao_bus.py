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
)
from app.domain.utils.validadores import (
    validar_assentos,
    validar_categoria,
    validar_datas,
    validar_duracao,
    validar_preco,
    validar_uf,
)


class SertaoBusStrategy(ViagemStrategy):

# Cada empresa manda um JSON com nomes de campos diferentes.
    def identifica(self, payload: dict[str, Any]) -> bool:
        return (
            "codigo" in payload
            and "de" in payload
            and "para" in payload
            and "embarque" in payload
            and "desembarque" in payload
        )

    def normaliza(
        self,
        payload: dict[str, Any],
    ) -> ViagemNormalizada:

        partida = converter_data(
            payload["embarque"],
            campo="embarque",
        )

        chegada = converter_data(
            payload["desembarque"],
            campo="desembarque",
        )

        duracao = converter_duracao(
            payload["duracao"]
        )

        preco_valor = self._converter_preco(
            payload["valor"]
        )

        categoria = self._normalizar_categoria(
            payload["tipo"]
        )

        assentos = converter_assentos(
            payload["lugares_livres"]
        )

        validar_datas(partida, chegada)
        validar_duracao(partida, chegada, duracao)
        validar_preco(preco_valor)
        validar_assentos(assentos)

        validar_uf(payload["de"]["sigla"])
        validar_uf(payload["para"]["sigla"])
        validar_categoria(categoria)

        preco = Preco(
            valor=preco_valor,
            moeda=payload["moeda"],
        )

        return ViagemNormalizada(
            id_viagem=payload["codigo"],
            empresa=self.nome_empresa(),

            origem=Localidade(
                cidade=payload["de"]["nome"],
                uf=payload["de"]["sigla"],
            ),

            destino=Localidade(
                cidade=payload["para"]["nome"],
                uf=payload["para"]["sigla"],
            ),

            partida=partida,
            chegada=chegada,

            duracao_minutos=duracao,

            preco=preco,

            categoria=categoria,

            assentos_disponiveis=assentos,
        )

    def nome_empresa(self) -> str:
        return "Sertão Bus"

    def _converter_preco(
        self,
        valor: str,
    ):
        from decimal import Decimal

        return Decimal(valor)

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