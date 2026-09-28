import time

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_desempenho_listagem_vulnerabilidades():
    quantidade_requisicoes = 100

    inicio = time.perf_counter()

    sucessos = 0
    erros = 0

    for _ in range(quantidade_requisicoes):
        response = client.get("/vulnerabilidades")

        if response.status_code == 200:
            sucessos += 1
        else:
            erros += 1

    fim = time.perf_counter()

    tempo_total = fim - inicio
    tempo_medio = tempo_total / quantidade_requisicoes
    requisicoes_por_segundo = quantidade_requisicoes / tempo_total

    print("\n===== TESTE DE DESEMPENHO =====")
    print(f"Requisições: {quantidade_requisicoes}")
    print(f"Sucessos: {sucessos}")
    print(f"Erros: {erros}")
    print(f"Tempo total: {tempo_total:.4f} segundos")
    print(f"Tempo médio: {tempo_medio:.6f} segundos")
    print(f"Requisições/segundo: {requisicoes_por_segundo:.2f}")
    print("===============================")

    assert erros == 0
    assert sucessos == quantidade_requisicoes