from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Ativo(Base):
    __tablename__ = "ativos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    tipo: Mapped[str] = mapped_column(String(50), nullable=False)
    endereco_ip: Mapped[str | None] = mapped_column(String(45), nullable=True)
    responsavel: Mapped[str | None] = mapped_column(String(100), nullable=True)
    status: Mapped[bool] = mapped_column(Boolean, default=True)