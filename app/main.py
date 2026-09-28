from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import Base, engine, SessionLocal
from app.models.ativo import Ativo
from app.models.responsavel import Responsavel
from app.models.vulnerabilidade import Vulnerabilidade

from app.schemas.ativo import AtivoCreate, AtivoResponse
from app.schemas.responsavel import ResponsavelCreate, ResponsavelResponse
from app.schemas.vulnerabilidade import (
    VulnerabilidadeCreate,
    VulnerabilidadeResponse,
    Criticidade,
    StatusVulnerabilidade
)


# Criação das tabelas
Base.metadata.create_all(bind=engine)


# Configuração da API
app = FastAPI(
    title="VulnTrack API",
    description="API para gerenciamento de vulnerabilidades de segurança",
    version="1.0.0"
)


# Conexão com o banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============================================================
# ROTA INICIAL
# ============================================================

@app.get("/")
def root():
    return {"message": "VulnTrack API funcionando!"}


# ============================================================
# ATIVOS
# ============================================================

@app.post("/ativos", response_model=AtivoResponse)
def criar_ativo(
    ativo: AtivoCreate,
    db: Session = Depends(get_db)
):
    novo_ativo = Ativo(**ativo.model_dump())

    db.add(novo_ativo)
    db.commit()
    db.refresh(novo_ativo)

    return novo_ativo


@app.get("/ativos", response_model=list[AtivoResponse])
def listar_ativos(
    db: Session = Depends(get_db)
):
    return db.query(Ativo).all()


@app.put("/ativos/{ativo_id}", response_model=AtivoResponse)
def atualizar_ativo(
    ativo_id: int,
    ativo: AtivoCreate,
    db: Session = Depends(get_db)
):
    ativo_existente = (
        db.query(Ativo)
        .filter(Ativo.id == ativo_id)
        .first()
    )

    if ativo_existente is None:
        raise HTTPException(
            status_code=404,
            detail="Ativo não encontrado"
        )

    ativo_existente.nome = ativo.nome
    ativo_existente.tipo = ativo.tipo
    ativo_existente.endereco_ip = ativo.endereco_ip
    ativo_existente.responsavel = ativo.responsavel
    ativo_existente.status = ativo.status

    db.commit()
    db.refresh(ativo_existente)

    return ativo_existente


@app.delete("/ativos/{ativo_id}")
def excluir_ativo(
    ativo_id: int,
    db: Session = Depends(get_db)
):
    ativo = (
        db.query(Ativo)
        .filter(Ativo.id == ativo_id)
        .first()
    )

    if ativo is None:
        raise HTTPException(
            status_code=404,
            detail="Ativo não encontrado"
        )

    db.delete(ativo)
    db.commit()

    return {
        "message": "Ativo excluído com sucesso",
        "id": ativo_id
    }


# ============================================================
# RESPONSÁVEIS
# ============================================================

@app.post("/responsaveis", response_model=ResponsavelResponse)
def criar_responsavel(
    responsavel: ResponsavelCreate,
    db: Session = Depends(get_db)
):
    novo_responsavel = Responsavel(
        **responsavel.model_dump()
    )

    db.add(novo_responsavel)
    db.commit()
    db.refresh(novo_responsavel)

    return novo_responsavel


@app.get("/responsaveis", response_model=list[ResponsavelResponse])
def listar_responsaveis(
    db: Session = Depends(get_db)
):
    return db.query(Responsavel).all()


@app.put(
    "/responsaveis/{responsavel_id}",
    response_model=ResponsavelResponse
)
def atualizar_responsavel(
    responsavel_id: int,
    responsavel: ResponsavelCreate,
    db: Session = Depends(get_db)
):
    responsavel_existente = (
        db.query(Responsavel)
        .filter(Responsavel.id == responsavel_id)
        .first()
    )

    if responsavel_existente is None:
        raise HTTPException(
            status_code=404,
            detail="Responsável não encontrado"
        )

    responsavel_existente.nome = responsavel.nome
    responsavel_existente.email = responsavel.email
    responsavel_existente.setor = responsavel.setor

    db.commit()
    db.refresh(responsavel_existente)

    return responsavel_existente


@app.delete("/responsaveis/{responsavel_id}")
def excluir_responsavel(
    responsavel_id: int,
    db: Session = Depends(get_db)
):
    responsavel = (
        db.query(Responsavel)
        .filter(Responsavel.id == responsavel_id)
        .first()
    )

    if responsavel is None:
        raise HTTPException(
            status_code=404,
            detail="Responsável não encontrado"
        )

    db.delete(responsavel)
    db.commit()

    return {
        "message": "Responsável excluído com sucesso",
        "id": responsavel_id
    }


# ============================================================
# VULNERABILIDADES
# ============================================================

@app.post(
    "/vulnerabilidades",
    response_model=VulnerabilidadeResponse
)
def criar_vulnerabilidade(
    vulnerabilidade: VulnerabilidadeCreate,
    db: Session = Depends(get_db)
):

    # Verifica se o responsável informado existe
    if vulnerabilidade.responsavel_id is not None:

        responsavel = (
            db.query(Responsavel)
            .filter(
                Responsavel.id == vulnerabilidade.responsavel_id
            )
            .first()
        )

        if responsavel is None:
            raise HTTPException(
                status_code=404,
                detail="Responsável informado não encontrado"
            )

    # Verifica se o ativo informado existe
    if vulnerabilidade.ativo_id is not None:

        ativo = (
            db.query(Ativo)
            .filter(
                Ativo.id == vulnerabilidade.ativo_id
            )
            .first()
        )

        if ativo is None:
            raise HTTPException(
                status_code=404,
                detail="Ativo informado não encontrado"
            )

    # Cria a vulnerabilidade
    nova_vulnerabilidade = Vulnerabilidade(
        **vulnerabilidade.model_dump()
    )

    db.add(nova_vulnerabilidade)
    db.commit()
    db.refresh(nova_vulnerabilidade)

    return nova_vulnerabilidade


@app.get(
    "/vulnerabilidades",
    response_model=list[VulnerabilidadeResponse]
)
def listar_vulnerabilidades(
    criticidade: Criticidade | None = Query(
        default=None,
        description="Filtra pela criticidade"
    ),

    status: StatusVulnerabilidade | None = Query(
        default=None,
        description="Filtra pelo status"
    ),

    titulo: str | None = Query(
        default=None,
        description="Busca parte do título"
    ),

    db: Session = Depends(get_db)
):

    consulta = db.query(Vulnerabilidade)

    if criticidade is not None:
        consulta = consulta.filter(
            Vulnerabilidade.criticidade == criticidade.value
        )

    if status is not None:
        consulta = consulta.filter(
            Vulnerabilidade.status == status.value
        )

    if titulo is not None:
        consulta = consulta.filter(
            Vulnerabilidade.titulo.ilike(
                f"%{titulo}%"
            )
        )

    return consulta.all()


@app.put(
    "/vulnerabilidades/{vulnerabilidade_id}",
    response_model=VulnerabilidadeResponse
)
def atualizar_vulnerabilidade(
    vulnerabilidade_id: int,
    vulnerabilidade: VulnerabilidadeCreate,
    db: Session = Depends(get_db)
):

    # Verifica se a vulnerabilidade existe
    vulnerabilidade_existente = (
        db.query(Vulnerabilidade)
        .filter(
            Vulnerabilidade.id == vulnerabilidade_id
        )
        .first()
    )

    if vulnerabilidade_existente is None:
        raise HTTPException(
            status_code=404,
            detail="Vulnerabilidade não encontrada"
        )

    # Verifica o responsável
    if vulnerabilidade.responsavel_id is not None:

        responsavel = (
            db.query(Responsavel)
            .filter(
                Responsavel.id == vulnerabilidade.responsavel_id
            )
            .first()
        )

        if responsavel is None:
            raise HTTPException(
                status_code=404,
                detail="Responsável informado não encontrado"
            )

    # Verifica o ativo
    if vulnerabilidade.ativo_id is not None:

        ativo = (
            db.query(Ativo)
            .filter(
                Ativo.id == vulnerabilidade.ativo_id
            )
            .first()
        )

        if ativo is None:
            raise HTTPException(
                status_code=404,
                detail="Ativo informado não encontrado"
            )

    # Atualiza os dados
    vulnerabilidade_existente.titulo = vulnerabilidade.titulo
    vulnerabilidade_existente.descricao = vulnerabilidade.descricao
    vulnerabilidade_existente.criticidade = vulnerabilidade.criticidade
    vulnerabilidade_existente.status = vulnerabilidade.status
    vulnerabilidade_existente.data_identificacao = (
        vulnerabilidade.data_identificacao
    )
    vulnerabilidade_existente.prazo_correcao = (
        vulnerabilidade.prazo_correcao
    )
    vulnerabilidade_existente.responsavel_id = (
        vulnerabilidade.responsavel_id
    )
    vulnerabilidade_existente.ativo_id = (
        vulnerabilidade.ativo_id
    )

    db.commit()
    db.refresh(vulnerabilidade_existente)

    return vulnerabilidade_existente


@app.delete("/vulnerabilidades/{vulnerabilidade_id}")
def excluir_vulnerabilidade(
    vulnerabilidade_id: int,
    db: Session = Depends(get_db)
):

    vulnerabilidade = (
        db.query(Vulnerabilidade)
        .filter(
            Vulnerabilidade.id == vulnerabilidade_id
        )
        .first()
    )

    if vulnerabilidade is None:
        raise HTTPException(
            status_code=404,
            detail="Vulnerabilidade não encontrada"
        )

    db.delete(vulnerabilidade)
    db.commit()

    return {
        "message": "Vulnerabilidade excluída com sucesso",
        "id": vulnerabilidade_id
    }