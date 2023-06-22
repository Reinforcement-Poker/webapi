from sqlalchemy import Column, Integer, String, Table
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedColumn, relationship


class Base(DeclarativeBase):
    pass


class Player(Base):
    __tablename__ = "player"

    id: Mapped[int] = MappedColumn(Integer, primary_key=True, nullable=False)
    username: Mapped[str] = MappedColumn(String(30), nullable=False)
    player_id: Mapped[int]


class State(Base):
    __tablename__ = "state"

    id: Mapped[int] = MappedColumn(Integer, primary_key=True, nullable=False)
    pot: Mapped[int] = MappedColumn(Integer, nullable=False)
    public_cards: Mapped[str] = MappedColumn(String(30), nullable=False)
