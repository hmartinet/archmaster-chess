from sqlalchemy.orm import Mapped, mapped_column


class BaseMetadata:
    __tablename__ = "metadata"

    key: Mapped[str] = mapped_column(primary_key=True)
    value: Mapped[str]
