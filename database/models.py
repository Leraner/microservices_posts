from uuid import UUID, uuid4
from sqlalchemy.orm import (
    DeclarativeBase,
    mapped_column,
    Mapped,
)
from datetime import datetime


class Base(DeclarativeBase):
    pass


class Post(Base):
    __tablename__ = "post"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column()
    author_id: Mapped[UUID] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
