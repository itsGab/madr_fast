from datetime import datetime

from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

table_registry = registry()


@table_registry.mapped_as_dataclass
class Usuario:
    __tablename__ = 'usuarios'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    senha: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)

    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    update_at: Mapped[datetime] = mapped_column(
        init=False, onupdate=func.now(), server_default=func.now()
    )


@table_registry.mapped_as_dataclass
class Livro:
    __tablename__ = 'livros'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    titulo: Mapped[str] = mapped_column(unique=True)
    ano: Mapped[int] = mapped_column()

    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    update_at: Mapped[datetime] = mapped_column(
        init=False, onupdate=func.now(), server_default=func.now()
    )

    romancista_id: Mapped[int] = mapped_column(ForeignKey('romancistas.id'))

    autoria: Mapped['Romancista'] = relationship(
        init=False, back_populates='livros'
    )


@table_registry.mapped_as_dataclass
class Romancista:
    __tablename__ = 'romancistas'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    nome: Mapped[str] = mapped_column(unique=True)

    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    update_at: Mapped[datetime] = mapped_column(
        init=False, onupdate=func.now(), server_default=func.now()
    )

    livros: Mapped[list['Livro']] = relationship(
        init=False, back_populates='romancistas', cascade='all, delete-orphan'
    )
