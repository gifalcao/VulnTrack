from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_rota_inicial():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "VulnTrack API funcionando!"
    }


def test_listar_ativos():
    response = client.get("/ativos")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_listar_responsaveis():
    response = client.get("/responsaveis")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_listar_vulnerabilidades():
    response = client.get("/vulnerabilidades")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_filtrar_vulnerabilidades_por_criticidade():
    response = client.get(
        "/vulnerabilidades",
        params={"criticidade": "Alta"}
    )

    assert response.status_code == 200

    vulnerabilidades = response.json()

    for vulnerabilidade in vulnerabilidades:
        assert vulnerabilidade["criticidade"] == "Alta"


def test_filtrar_vulnerabilidades_por_status():
    response = client.get(
        "/vulnerabilidades",
        params={"status": "Em tratamento"}
    )

    assert response.status_code == 200

    vulnerabilidades = response.json()

    for vulnerabilidade in vulnerabilidades:
        assert vulnerabilidade["status"] == "Em tratamento"


def test_buscar_vulnerabilidade_por_titulo():
    response = client.get(
        "/vulnerabilidades",
        params={"titulo": "Apache"}
    )

    assert response.status_code == 200

    vulnerabilidades = response.json()

    for vulnerabilidade in vulnerabilidades:
        assert "apache" in vulnerabilidade["titulo"].lower()


def test_responsavel_inexistente():
    dados = {
        "titulo": "Teste automatizado",
        "descricao": "Teste de responsável inexistente",
        "criticidade": "Alta",
        "status": "Aberta",
        "data_identificacao": "2026-09-28",
        "prazo_correcao": "2026-10-05",
        "responsavel_id": 999,
        "ativo_id": 1
    }

    response = client.post(
        "/vulnerabilidades",
        json=dados
    )

    assert response.status_code == 404
    assert response.json()["detail"] == (
        "Responsável informado não encontrado"
    )


def test_ativo_inexistente():
    dados = {
        "titulo": "Teste automatizado",
        "descricao": "Teste de ativo inexistente",
        "criticidade": "Alta",
        "status": "Aberta",
        "data_identificacao": "2026-09-28",
        "prazo_correcao": "2026-10-05",
        "responsavel_id": 1,
        "ativo_id": 999
    }

    response = client.post(
        "/vulnerabilidades",
        json=dados
    )

    assert response.status_code == 404
    assert response.json()["detail"] == (
        "Ativo informado não encontrado"
    )


def test_data_invalida():
    dados = {
        "titulo": "Teste automatizado",
        "descricao": "Teste de data inválida",
        "criticidade": "Baixa",
        "status": "Aberta",
        "data_identificacao": "28/09/2026",
        "prazo_correcao": "05/10/2026",
        "responsavel_id": 1,
        "ativo_id": 1
    }

    response = client.post(
        "/vulnerabilidades",
        json=dados
    )

    assert response.status_code == 422