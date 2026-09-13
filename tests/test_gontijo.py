from decimal import Decimal

from app.domain.strategies.gontijo import GontijoStrategy


def test_normaliza_gontijo_valido():
    payload = {
        "reserva": "GON-2026-455",
        "embarque": {
            "cidade": "Paulo Afonso",
            "uf": "BA",
        },
        "desembarque": {
            "cidade": "Salvador",
            "uf": "BA",
        },
        "saida": "2026-10-15T08:00:00-03:00",
        "chegada": "2026-10-15T15:30:00-03:00",
        "duracao": 450,
        "preco_centavos": 14990,
        "moeda": "BRL",
        "servico": "SEMI",
        "assentos": "16",
    }

    strategy = GontijoStrategy()

    viagem = strategy.normaliza(payload)

    assert viagem.id_viagem == "GON-2026-455"
    assert viagem.empresa == "Gontijo"

    assert viagem.origem.cidade == "Paulo Afonso"
    assert viagem.origem.uf == "BA"

    assert viagem.destino.cidade == "Salvador"
    assert viagem.destino.uf == "BA"

    assert viagem.duracao_minutos == 450

    assert viagem.preco.valor == Decimal("149.90")
    assert viagem.preco.moeda == "BRL"

    assert viagem.categoria == "semileito"
    assert viagem.assentos_disponiveis == 16