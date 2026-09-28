\# VulnTrack



Sistema de Gestão de Vulnerabilidades desenvolvido como Projeto Integrador – Web Services.



\## 1. Sobre o projeto



O VulnTrack é uma API REST desenvolvida para auxiliar pequenas e médias organizações no registro, acompanhamento e tratamento de vulnerabilidades de segurança.



A solução centraliza informações sobre:



\- Ativos;

\- Responsáveis;

\- Vulnerabilidades;

\- Criticidade;

\- Status de tratamento;

\- Datas de identificação;

\- Prazos de correção.



O objetivo é facilitar a organização do processo de tratamento de vulnerabilidades e reduzir a dependência de planilhas e registros descentralizados.



\---



\## 2. Objetivo



Desenvolver uma API REST capaz de realizar o cadastro, consulta, atualização e exclusão de informações relacionadas ao gerenciamento de vulnerabilidades.



\### Objetivos específicos



\- Implementar operações CRUD;

\- Cadastrar ativos;

\- Cadastrar responsáveis;

\- Cadastrar vulnerabilidades;

\- Relacionar vulnerabilidades a ativos e responsáveis;

\- Classificar vulnerabilidades por criticidade;

\- Controlar o status de tratamento;

\- Permitir filtros e buscas;

\- Disponibilizar documentação Swagger/OpenAPI;

\- Implementar testes automatizados;

\- Realizar testes de desempenho;

\- Disponibilizar ambiente de execução utilizando Docker.



\---



\## 3. Tecnologias utilizadas



\### Backend



\- Python 3.14

\- FastAPI

\- Uvicorn

\- SQLAlchemy

\- Pydantic



\### Banco de dados



\- SQLite



\### Testes



\- Pytest

\- FastAPI TestClient



\### Documentação



\- Swagger/OpenAPI



\### Infraestrutura



\- Docker

\- Docker Compose

\- WSL 2



\### Versionamento



\- Git

\- GitHub



\---



\## 4. Arquitetura



A aplicação utiliza uma arquitetura organizada em camadas:



```text

VulnTrack

│

├── app/

│   ├── main.py

│   ├── database.py

│   │

│   ├── models/

│   │   ├── ativo.py

│   │   ├── responsavel.py

│   │   └── vulnerabilidade.py

│   │

│   └── schemas/

│       ├── ativo.py

│       ├── responsavel.py

│       └── vulnerabilidade.py

│

├── tests/

│   ├── test\_api.py

│   └── test\_performance.py

│

├── Dockerfile

├── docker-compose.yml

├── requirements.txt

├── pytest.ini

└── README.md

