from pydantic import BaseModel, ConfigDict


class ResponsavelBase(BaseModel):
    nome: str
    email: str
    setor: str


class ResponsavelCreate(ResponsavelBase):
    pass


class ResponsavelResponse(ResponsavelBase):
    id: int

    model_config = ConfigDict(from_attributes=True)