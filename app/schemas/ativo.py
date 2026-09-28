from pydantic import BaseModel, ConfigDict


class AtivoBase(BaseModel):
    nome: str
    tipo: str
    endereco_ip: str | None = None
    responsavel: str | None = None
    status: bool = True


class AtivoCreate(AtivoBase):
    pass


class AtivoResponse(AtivoBase):
    id: int

    model_config = ConfigDict(from_attributes=True)