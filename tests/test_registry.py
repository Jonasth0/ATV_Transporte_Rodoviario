from app.domain.registry import StrategyRegistry
from app.domain.strategies.gontijo import GontijoStrategy
from app.domain.strategies.progresso import ProgressoStrategy
from app.domain.strategies.rota import RotaStrategy


def test_identifica_progresso():
    payload = {
        "codigoViagem": "PRG-2026-001",
        "cidadeOrigem": "Paulo Afonso",
        "ufOrigem": "BA",
        "cidadeDestino": "Recife",
        "ufDestino": "PE",
        "dataHoraSaida": "15/10/2026 06:30",
        "dataHoraChegada": "15/10/2026 12:50",
    }

    registry = StrategyRegistry()

    strategy = registry.identificar(payload)

    assert isinstance(strategy, ProgressoStrategy)


def test_identifica_rota():
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

    registry = StrategyRegistry()

    strategy = registry.identificar(payload)

    assert isinstance(strategy, RotaStrategy)


def test_identifica_gontijo():
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
    }

    registry = StrategyRegistry()

    strategy = registry.identificar(payload)

    assert isinstance(strategy, GontijoStrategy)


def test_formato_desconhecido():
    payload = {
        "empresa": "Empresa Desconhecida",
        "viagem": "XYZ-123",
    }

    registry = StrategyRegistry()

    strategy = registry.identificar(payload)

    assert strategy is None