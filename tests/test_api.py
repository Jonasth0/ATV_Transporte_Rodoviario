from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_normaliza_viagens_validas():
    payload = [
        {
            "codigoViagem": "PRG-2026-001",
            "cidadeOrigem": "Paulo Afonso",
            "ufOrigem": "BA",
            "cidadeDestino": "Recife",
            "ufDestino": "PE",
            "dataHoraSaida": "15/10/2026 06:30",
            "dataHoraChegada": "15/10/2026 12:50",
            "tempoEstimado": "06:20",
            "valorPassagem": "129,90",
            "tipoServico": "EXECUTIVO",
            "assentosDisponiveis": "18",
        },
        {
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
        },
    ]

    response = client.post(
        "/api/v1/viagens/normalizar",
        json=payload,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 2
    assert len(data["viagens"]) == 2

    assert data["viagens"][0]["empresa"] == "Auto Viação Progresso"
    assert data["viagens"][1]["empresa"] == "Rota Transportes"

def test_rejeita_chegada_anterior_a_partida():
    payload = [
        {
            "trip_id": "ROT-2026-999",
            "origem": {
                "municipio": "Paulo Afonso",
                "estado": "BA",
            },
            "destino": {
                "municipio": "Aracaju",
                "estado": "SE",
            },
            "partida_em": "2026-10-15T12:00:00-03:00",
            "chegada_em": "2026-10-15T10:00:00-03:00",
            "duracao_minutos": 120,
            "tarifa_centavos": 8990,
            "moeda": "BRL",
            "classe": "convencional",
            "vagas": 22,
        }
    ]

    response = client.post(
        "/api/v1/viagens/normalizar",
        json=payload,
    )

    assert response.status_code == 422

    data = response.json()

    assert data == {
        "detail": {
            "indice": 0,
            "empresa_identificada": "Rota Transportes",
            "campo": "chegada_em",
            "mensagem": (
                "A data de chegada deve ser posterior "
                "à data de saída."
            ),
        }
    }

def test_rejeita_toda_requisicao_se_uma_viagem_for_invalida():
    payload = [
        {
            "codigoViagem": "PRO-001",
            "cidadeOrigem": "Petrolândia",
            "ufOrigem": "PE",
            "cidadeDestino": "Paulo Afonso",
            "ufDestino": "BA",
            "dataHoraSaida": "15/10/2026 06:30",
            "dataHoraChegada": "15/10/2026 12:50",
            "tempoEstimado": "06:20",
            "valorPassagem": "129,90",
            "tipoServico": "EXECUTIVO",
            "assentosDisponiveis": 18,
        },
        {
            "trip_id": "ROTA-002",
            "origem": {
                "municipio": "Recife",
                "estado": "PE",
            },
            "destino": {
                "municipio": "Maceió",
                "estado": "AL",
            },
            "partida_em": "2026-10-15T14:00:00-03:00",
            "chegada_em": "2026-10-15T12:00:00-03:00",
            "duracao_minutos": 240,
            "tarifa_centavos": 8990,
            "moeda": "BRL",
            "classe": "executivo",
            "vagas": 10,
        },
    ]

    response = client.post(
        "/api/v1/viagens/normalizar",
        json=payload,
    )

    assert response.status_code == 422

    assert response.json() == {
        "detail": {
            "indice": 1,
            "empresa_identificada": "Rota Transportes",
            "campo": "chegada_em",
            "mensagem": (
                "A data de chegada deve ser posterior "
                "à data de saída."
            ),
        }
    }

def test_normaliza_sertao_bus_pelo_endpoint():
    payload = [
        {
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
    ]

    response = client.post(
        "/api/v1/viagens/normalizar",
        json=payload,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 1

    viagem = data["viagens"][0]

    assert viagem["id_viagem"] == "SB-2026-001"
    assert viagem["empresa"] == "Sertão Bus"

    assert viagem["origem"] == {
        "cidade": "Petrolândia",
        "uf": "PE",
    }

    assert viagem["destino"] == {
        "cidade": "Paulo Afonso",
        "uf": "BA",
    }

    assert viagem["duracao_minutos"] == 210
    assert viagem["preco"]["valor"] == "75.50"
    assert viagem["preco"]["moeda"] == "BRL"
    assert viagem["categoria"] == "leito"
    assert viagem["assentos_disponiveis"] == 12