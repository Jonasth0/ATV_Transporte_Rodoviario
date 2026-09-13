from decimal import Decimal

from app.domain.strategies.rota import RotaStrategy


def test_normaliza_rota_valida():
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
        "duracao_minutos": 310,
        "tarifa_centavos": 8990,
        "moeda": "BRL",
        "classe": "convencional",
        "vagas": 22,
    }

    strategy = RotaStrategy()

    viagem = strategy.normaliza(payload)

    assert viagem.id_viagem == "ROT-2026-872"
    assert viagem.empresa == "Rota Transportes"

    assert viagem.origem.cidade == "Paulo Afonso"
    assert viagem.origem.uf == "BA"

    assert viagem.destino.cidade == "Aracaju"
    assert viagem.destino.uf == "SE"

    assert viagem.duracao_minutos == 310

    assert viagem.preco.valor == Decimal("89.90")
    assert viagem.preco.moeda == "BRL"

    assert viagem.categoria == "convencional"
    assert viagem.assentos_disponiveis == 22