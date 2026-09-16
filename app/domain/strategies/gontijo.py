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
    converter_preco_centavos,
)
from app.domain.utils.validadores import (
    validar_assentos,
    validar_categoria,
    validar_datas,
    validar_duracao,
    validar_preco,
    validar_uf,
)


class GontijoStrategy(ViagemStrategy):

# Cada empresa manda um JSON com nomes de campos diferentes.
    def identifica(self, payload: dict[str, Any]) -> bool:
        return (
            "reserva" in payload
            and "embarque" in payload
            and "desembarque" in payload
            and "saida" in payload
            and "chegada" in payload
        )

    def normaliza(
        self,
        payload: dict[str, Any],
    ) -> ViagemNormalizada:

        partida = converter_data(
            payload["saida"],
            campo="saida",
        )

        chegada = converter_data(
            payload["chegada"],
            campo="chegada",
        )

        duracao = converter_duracao(
            payload["duracao"]
        )

        preco_valor = converter_preco_centavos(
            payload["preco_centavos"]
        )

        categoria = self._normalizar_categoria(
            payload["servico"]
        )

        assentos = converter_assentos(
            payload["assentos"]
        )

        validar_datas(partida, chegada)
        validar_duracao(partida, chegada, duracao)
        validar_preco(preco_valor)
        validar_assentos(assentos)

        validar_uf(payload["embarque"]["uf"])
        validar_uf(payload["desembarque"]["uf"])
        validar_categoria(categoria)

        preco = Preco(
            valor=preco_valor,
            moeda=payload["moeda"],
        )

        return ViagemNormalizada(
            id_viagem=payload["reserva"],
            empresa=self.nome_empresa(),

            origem=Localidade(
                cidade=payload["embarque"]["cidade"],
                uf=payload["embarque"]["uf"],
            ),

            destino=Localidade(
                cidade=payload["desembarque"]["cidade"],
                uf=payload["desembarque"]["uf"],
            ),

            partida=partida,
            chegada=chegada,

            duracao_minutos=duracao,

            preco=preco,

            categoria=categoria,

            assentos_disponiveis=assentos,
        )

    def nome_empresa(self) -> str:
        return "Gontijo"

    def _normalizar_categoria(
        self,
        valor: str,
    ) -> str:

        categorias = {
            "CONV": "convencional",
            "EXEC": "executivo",
            "SEMI": "semileito",
            "LEITO": "leito",
        }

        categoria = categorias.get(valor.upper())

        if categoria is None:
            raise ValueError("Categoria inválida.")

        return categoria