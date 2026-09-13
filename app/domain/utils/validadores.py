from datetime import datetime
from decimal import Decimal

from app.exceptions.viagem import ViagemValidationError


CATEGORIAS_VALIDAS = {
    "convencional",
    "executivo",
    "semileito",
    "leito",
}


def validar_datas(
    partida: datetime,
    chegada: datetime,
):
    if chegada <= partida:
        raise ViagemValidationError(
            campo="chegada_em",
            mensagem=(
                "A data de chegada deve ser posterior "
                "à data de saída."
            ),
        )


def validar_duracao(
    partida: datetime,
    chegada: datetime,
    duracao_minutos: int,
):
    if duracao_minutos <= 0:
        raise ViagemValidationError(
            campo="duracao",
            mensagem="A duração da viagem deve ser maior que zero.",
        )

    duracao_real = (
        chegada - partida
    ).total_seconds() / 60

    if duracao_real != duracao_minutos:
        raise ViagemValidationError(
            campo="duracao",
            mensagem=(
                "A duração informada é incompatível "
                "com os horários de saída e chegada."
            ),
        )

def validar_preco(
    preco: Decimal,
):
    if preco <= 0:
        raise ViagemValidationError(
            campo="preco",
            mensagem="O preço da viagem deve ser maior que zero.",
        )


def validar_assentos(
    assentos: int,
):
    if assentos < 0:
        raise ViagemValidationError(
            campo="assentos",
            mensagem="A quantidade de assentos não pode ser negativa.",
        )


def validar_uf(
    uf: str,
):
    if len(uf) != 2:
        raise ViagemValidationError(
            campo="uf",
            mensagem="A UF deve possuir exatamente dois caracteres.",
        )


def validar_categoria(
    categoria: str,
):
    if categoria not in CATEGORIAS_VALIDAS:
        raise ViagemValidationError(
            campo="categoria",
            mensagem="A categoria da viagem é inválida.",
        )