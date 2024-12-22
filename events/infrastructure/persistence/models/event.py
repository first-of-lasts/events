from datetime import datetime

from sqlalchemy import String, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from events.infrastructure.persistence.manager import Base


class Event(Base):
    __tablename__ = "events"

    title: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(2048), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    #
    organizer_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    # organizer: Mapped["User"] = relationship(
    #     "User", back_populates="created_events"
    # )
