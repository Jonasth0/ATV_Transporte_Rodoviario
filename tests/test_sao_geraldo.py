from decimal import Decimal

from app.domain.strategies.sao_geraldo import SaoGeraldoStrategy


def test_normaliza_viagem_sao_geraldo():

    payload = {
        "codigoServico": "SGR-2026-321",
        "localEmbarque": {
            "municipio": "Paulo Afonso",
            "uf": "BA",
        },
        "localDesembarque": {
            "municipio": "Juazeiro",
            "uf": "BA",
        },
        "horarioPartida": "2026-10-15 09:15",
        "horarioChegada": "2026-10-15 10:45",
        "tempoViagemMinutos": 90,
        "precoPassagem": "45,00",
        "moedaPagamento": "BRL",
        "tipoAssento": "Convencional",
        "vagasDisponiveis": 30,
    }

    strategy = SaoGeraldoStrategy()

    viagem = strategy.normaliza(payload)

    assert viagem.id_viagem == "SGR-2026-321"
    assert viagem.empresa == "São Geraldo"

    assert viagem.origem.cidade == "Paulo Afonso"
    assert viagem.origem.uf == "BA"

    assert viagem.destino.cidade == "Juazeiro"
    assert viagem.destino.uf == "BA"

    assert viagem.duracao_minutos == 90
    assert viagem.preco.valor == Decimal("45.00")
    assert viagem.preco.moeda == "BRL"

    assert viagem.categoria == "convencional"
    assert viagem.assentos_disponiveis == 30


def test_identifica_payload_sao_geraldo():

    payload = {
        "codigoServico": "SGR-2026-321",
        "localEmbarque": {
            "municipio": "Paulo Afonso",
            "uf": "BA",
        },
        "localDesembarque": {
            "municipio": "Juazeiro",
            "uf": "BA",
        },
        "horarioPartida": "2026-10-15 09:15",
        "horarioChegada": "2026-10-15 10:45",
    }

    strategy = SaoGeraldoStrategy()

    assert strategy.identifica(payload) is True


def test_nao_identifica_payload_de_outra_empresa():

    payload = {
        "trip_id": "ROT-2026-872",
        "origem": {
            "municipio": "Paulo Afonso",
            "estado": "BA",
        },
        "destino": {
            "municipio": "Aracaju",
            "estado": "SE",
        },
        "partida_em": "2026-10-15T07:00:00-03:00",
        "chegada_em": "2026-10-15T12:10:00-03:00",
    }

    strategy = SaoGeraldoStrategy()

    assert strategy.identifica(payload) is False
