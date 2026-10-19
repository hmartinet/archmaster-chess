from datetime import date

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from archmaster.database.base import BaseSession

from .game_base_migration import GameBaseMigration


class GameBase(DeclarativeBase):
    pass


class GameMetadata(GameBase):
    __tablename__ = "metadata"

    key: Mapped[str] = mapped_column(primary_key=True)
    value: Mapped[str]


class Game(GameBase):
    __tablename__ = "game"

    id: Mapped[int] = mapped_column(primary_key=True)
    event: Mapped[str]
    site: Mapped[str]
    date_at: Mapped[date | None]
    round: Mapped[int | None]
    white: Mapped[str]
    black: Mapped[str]
    result: Mapped[int]
    white_elo: Mapped[int | None]
    black_elo: Mapped[int | None]
    white_title: Mapped[str]
    black_title: Mapped[str]
    eco: Mapped[str]
    time_control: Mapped[str]
    source: Mapped[str]
    pgn: Mapped[bytes]


class GameBaseSession(GameBaseMigration, BaseSession):
    _base = GameBase
    _version = 1
