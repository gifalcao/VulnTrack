from datetime import date
from enum import Enum

from pydantic import BaseModel, ConfigDict


class Criticidade(str, Enum):
    BAIXA = "Baixa"
    MEDIA = "Média"
    ALTA = "Alta"
    CRITICA = "Crítica"


class StatusVulnerabilidade(str, Enum):
    ABERTA = "Aberta"
    EM_TRATAMENTO = "Em tratamento"
    CORRIGIDA = "Corrigida"


class VulnerabilidadeBase(BaseModel):
    titulo: str
    descricao: str
    criticidade: Criticidade
    status: StatusVulnerabilidade
    data_identificacao: date
    prazo_correcao: date | None = None
    responsavel_id: int | None = None
    ativo_id: int | None = None


class VulnerabilidadeCreate(VulnerabilidadeBase):
    pass


class VulnerabilidadeResponse(VulnerabilidadeBase):
    id: int

    model_config = ConfigDict(from_attributes=True)