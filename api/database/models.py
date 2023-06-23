from sqlalchemy import Column, Integer, String, Table
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedColumn, relationship


class Base(DeclarativeBase):
    pass


class Player(Base):
    __tablename__ = "player"

    id: Mapped[int] = MappedColumn(Integer, primary_key=True, nullable=False)
    username: Mapped[str] = MappedColumn(String(30), nullable=False)


class State(Base):
    __tablename__ = "state"

    id: Mapped[int] = MappedColumn(Integer, primary_key=True, nullable=False)
    game_id: Mapped[int] = MappedColumn(Integer, nullable=False)
    stage: Mapped[str] = MappedColumn(String(30), nullable=False)
    pot: Mapped[int] = MappedColumn(Integer, nullable=False)
    public_cards: Mapped[str] = MappedColumn(String(30), nullable=False)


class Game(Base):
    __tablename__ = "game"

    id: Mapped[int] = MappedColumn(Integer, primary_key=True, nullable=False)
    n_players: Mapped[int] = MappedColumn(Integer, nullable=False)
    states: Mapped[list["State"]] = relationship(
        "State",
        primaryjoin="foreign(Game.id) == State.game_id",
        backref="game",
    )


class Bet(Base):
    __tablename__ = "bet"

    state_id: Mapped[int] = MappedColumn(Integer, primary_key=True, nullable=False)
    player_id: Mapped[int] = MappedColumn(Integer, primary_key=True, nullable=False)

    action: Mapped[str] = MappedColumn(String(30), nullable=False)
    chips: Mapped[int] = MappedColumn(Integer, nullable=False)

    players: Mapped[list["Player"]] = relationship(
        "Player",
        primaryjoin="foreign(Bet.player_id) == Player.id",
    )
    states: Mapped[list["State"]] = relationship(
        "State",
        primaryjoin="foreign(Bet.state_id) == State.id",
    )
