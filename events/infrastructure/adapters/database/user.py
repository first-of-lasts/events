from sqlalchemy import String, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from events.infrastructure.adapters.database.manager import Base


class User(Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    bio: Mapped[str] = mapped_column(Text, nullable=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    is_admin: Mapped[bool]  = mapped_column(Boolean, default=False)
    # created_events = relationship("Event", back_populates="organizer")
