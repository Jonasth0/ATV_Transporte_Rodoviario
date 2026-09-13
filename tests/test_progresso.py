from decimal import Decimal

from app.domain.strategies.progresso import ProgressoStrategy


def test_normaliza_progresso_valido():
    payload = {
        "codigoViagem": "PRG-2026-001",
        "cidadeOrigem": "Paulo Afonso",
        "ufOrigem": "BA",
        "cidadeDestino": "Recife",
        "ufDestino": "PE",
        "dataHoraSaida": "15/10/2026 06:30",
        "dataHoraChegada": "15/10/2026 12:50",
        "fusoHorario": "America/Bahia",
        "tempoEstimado": "06:20",
        "valorPassagem": "129,90",
        "tipoServico": "EXECUTIVO",
        "assentosDisponiveis": "18",
    }

    strategy = ProgressoStrategy()

    viagem = strategy.normaliza(payload)

    assert viagem.id_viagem == "PRG-2026-001"
    assert viagem.empresa == "Auto Viação Progresso"

    assert viagem.origem.cidade == "Paulo Afonso"
    assert viagem.origem.uf == "BA"

    assert viagem.destino.cidade == "Recife"
    assert viagem.destino.uf == "PE"

    assert viagem.duracao_minutos == 380

    assert viagem.preco.valor == Decimal("129.90")
    assert viagem.preco.moeda == "BRL"

    assert viagem.categoria == "executivo"
    assert viagem.assentos_disponiveis == 18