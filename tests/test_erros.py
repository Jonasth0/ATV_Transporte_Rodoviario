from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def payload_rota():
    return {
        "trip_id": "ROT-001",
        "origem": {
            "municipio": "Petrolândia",
            "estado": "PE",
        },
        "destino": {
            "municipio": "Paulo Afonso",
            "estado": "BA",
        },
        "partida_em": "2026-10-20T08:00:00",
        "chegada_em": "2026-10-20T11:00:00",
        "duracao_minutos": 180,
        "tarifa_centavos": 5000,
        "classe": "convencional",
        "vagas": 10,
        "moeda": "BRL",
    }


def test_rejeita_data_invalida():
    payload = payload_rota()
    payload["partida_em"] = "data inválida"

    response = client.post(
        "/api/v1/viagens/normalizar",
        json=[payload],
    )

    assert response.status_code == 422

    assert response.json()["detail"]["campo"] == "partida_em"


def test_rejeita_duracao_invalida():
    payload = payload_rota()
    payload["duracao_minutos"] = "abc"

    response = client.post(
        "/api/v1/viagens/normalizar",
        json=[payload],
    )

    assert response.status_code == 422


def test_rejeita_preco_invalido():
    payload = payload_rota()
    payload["tarifa_centavos"] = "abc"

    response = client.post(
        "/api/v1/viagens/normalizar",
        json=[payload],
    )

    assert response.status_code == 422


def test_rejeita_assentos_negativos():
    payload = payload_rota()
    payload["vagas"] = -5

    response = client.post(
        "/api/v1/viagens/normalizar",
        json=[payload],
    )

    assert response.status_code == 422


def test_rejeita_uf_invalida():
    payload = payload_rota()
    payload["origem"]["estado"] = "P"

    response = client.post(
        "/api/v1/viagens/normalizar",
        json=[payload],
    )

    assert response.status_code == 422


def test_rejeita_categoria_invalida():
    payload = payload_rota()
    payload["classe"] = "premium espacial"

    response = client.post(
        "/api/v1/viagens/normalizar",
        json=[payload],
    )

    assert response.status_code == 422


def test_rejeita_duracao_incompativel():
    payload = payload_rota()
    payload["duracao_minutos"] = 100

    response = client.post(
        "/api/v1/viagens/normalizar",
        json=[payload],
    )

    assert response.status_code == 422


def test_rejeita_chegada_antes_da_saida():
    payload = payload_rota()
    payload["chegada_em"] = "2026-10-20T07:00:00"

    response = client.post(
        "/api/v1/viagens/normalizar",
        json=[payload],
    )

    assert response.status_code == 422


def test_rejeita_preco_zero():
    payload = payload_rota()
    payload["tarifa_centavos"] = 0

    response = client.post(
        "/api/v1/viagens/normalizar",
        json=[payload],
    )

    assert response.status_code == 422


def test_rejeita_formato_desconhecido():
    payload = {
        "coisa": "qualquer",
        "outro_campo": 123,
    }

    response = client.post(
        "/api/v1/viagens/normalizar",
        json=[payload],
    )

    assert response.status_code == 422

    detail = response.json()["detail"]

    assert detail["indice"] == 0
    assert detail["empresa_identificada"] is None
    assert detail["campo"] is None
    assert (
        detail["mensagem"]
        == "O formato do payload não corresponde "
        "a nenhuma companhia suportada."
    )