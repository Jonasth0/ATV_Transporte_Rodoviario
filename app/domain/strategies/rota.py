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

        partida = converter_data(
            payload["partida_em"],
            campo="partida_em",
        )

        chegada = converter_data(
            payload["chegada_em"],
            campo="chegada_em",
        )

        duracao = converter_duracao(
            payload["duracao_minutos"]
        )

        preco_valor = converter_preco_centavos(
            payload["tarifa_centavos"]
        )

        categoria = self._normalizar_categoria(
            payload["classe"]
        )

        assentos = converter_assentos(
            payload["vagas"]
        )

        validar_datas(partida, chegada)
        validar_duracao(partida, chegada, duracao)
        validar_preco(preco_valor)
        validar_assentos(assentos)

        validar_uf(payload["origem"]["estado"])
        validar_uf(payload["destino"]["estado"])
        validar_categoria(categoria)

        preco = Preco(
            valor=preco_valor,
            moeda=payload["moeda"],
        )

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

            duracao_minutos=duracao,

            preco=preco,

            categoria=categoria,

            assentos_disponiveis=assentos,
        )

    def nome_empresa(self) -> str:
        return "Rota Transportes"

    def _normalizar_categoria(
        self,
        valor: str,
    ) -> str:

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