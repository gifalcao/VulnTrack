from datetime import date

from sqlalchemy import Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Vulnerabilidade(Base):
    __tablename__ = "vulnerabilidades"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    titulo: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    descricao: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    criticidade: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    data_identificacao: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    prazo_correcao: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )

    responsavel_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("responsaveis.id"),
        nullable=True
    )

    ativo_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("ativos.id"),
        nullable=True
    )