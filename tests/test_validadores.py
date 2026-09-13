from datetime import datetime
from decimal import Decimal

import pytest

from app.domain.utils.validadores import (
    validar_assentos,
    validar_categoria,
    validar_datas,
    validar_duracao,
    validar_preco,
    validar_uf,
)
from app.exceptions.viagem import ViagemValidationError


def test_rejeita_chegada_antes_da_partida():
    partida = datetime(2026, 10, 15, 10, 0)
    chegada = datetime(2026, 10, 15, 9, 0)

    with pytest.raises(ViagemValidationError):
        validar_datas(partida, chegada)


def test_rejeita_duracao_zero():
    with pytest.raises(ViagemValidationError):
        validar_duracao(0)


def test_rejeita_duracao_negativa():
    partida = datetime(2026, 10, 15, 8, 0)
    chegada = datetime(2026, 10, 15, 9, 0)

    with pytest.raises(ViagemValidationError):
        validar_duracao(
            partida,
            chegada,
            -10,
        )


def test_rejeita_duracao_zero():
    partida = datetime(2026, 10, 15, 8, 0)
    chegada = datetime(2026, 10, 15, 9, 0)

    with pytest.raises(ViagemValidationError):
        validar_duracao(
            partida,
            chegada,
            0,
        )


def test_rejeita_preco_negativo():
    with pytest.raises(ViagemValidationError):
        validar_preco(Decimal("-10.00"))


def test_rejeita_assentos_negativos():
    with pytest.raises(ViagemValidationError):
        validar_assentos(-1)


def test_rejeita_uf_invalida():
    with pytest.raises(ViagemValidationError):
        validar_uf("BAH")


def test_rejeita_categoria_invalida():
    with pytest.raises(ViagemValidationError):
        validar_categoria("premium")

def test_rejeita_duracao_incompativel_com_horarios():
    partida = datetime(2026, 10, 15, 8, 0)
    chegada = datetime(2026, 10, 15, 11, 30)

    with pytest.raises(ViagemValidationError) as erro:
        validar_duracao(
            partida,
            chegada,
            240,
        )

    assert erro.value.campo == "duracao"
    assert erro.value.mensagem == (
        "A duração informada é incompatível "
        "com os horários de saída e chegada."
    )

def test_aceita_duracao_compativel_com_horarios():
    partida = datetime(2026, 10, 15, 8, 0)
    chegada = datetime(2026, 10, 15, 11, 30)

    validar_duracao(
        partida,
        chegada,
        210,
    )