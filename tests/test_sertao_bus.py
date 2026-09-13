from decimal import Decimal

from app.domain.strategies.sertao_bus import SertaoBusStrategy


def test_normaliza_viagem_sertao_bus():

    payload = {
        "codigo": "SB-2026-001",
        "de": {
            "nome": "Petrolândia",
            "sigla": "PE",
        },
        "para": {
            "nome": "Paulo Afonso",
            "sigla": "BA",
        },
        "embarque": "2026-10-20T08:00:00",
        "desembarque": "2026-10-20T11:30:00",
        "duracao": "03:30",
        "valor": "75.50",
        "tipo": "Leito",
        "lugares_livres": "12",
        "moeda": "BRL",
    }

    strategy = SertaoBusStrategy()

    viagem = strategy.normaliza(payload)

    assert viagem.id_viagem == "SB-2026-001"
    assert viagem.empresa == "Sertão Bus"

    assert viagem.origem.cidade == "Petrolândia"
    assert viagem.origem.uf == "PE"

    assert viagem.destino.cidade == "Paulo Afonso"
    assert viagem.destino.uf == "BA"

    assert viagem.duracao_minutos == 210
    assert viagem.preco.valor == Decimal("75.50")
    assert viagem.preco.moeda == "BRL"

    assert viagem.categoria == "leito"
    assert viagem.assentos_disponiveis == 12

def test_identifica_payload_sertao_bus():

    payload = {
        "codigo": "SB-2026-001",
        "de": {
            "nome": "Petrolândia",
            "sigla": "PE",
        },
        "para": {
            "nome": "Paulo Afonso",
            "sigla": "BA",
        },
        "embarque": "2026-10-20T08:00:00",
        "desembarque": "2026-10-20T11:30:00",
    }

    strategy = SertaoBusStrategy()

    assert strategy.identifica(payload) is True