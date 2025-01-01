from datetime import datetime

from sqlalchemy import String, Boolean, Integer, ForeignKey, DateTime, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from events.infrastructure.persistence.manager import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        Index("idx_users_country_id", "country_id"),
        Index("idx_users_region_id", "region_id"),
    )

    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    bio: Mapped[str] = mapped_column(String(2048), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    is_admin: Mapped[bool]  = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    # Foreign Keys
    country_id: Mapped[int] = mapped_column(Integer, ForeignKey("countries.id"), nullable=True)
    region_id: Mapped[int] = mapped_column(Integer, ForeignKey("regions.id"), nullable=True)
    # Relationships
    country = relationship(argument="Country", back_populates="users")
    region = relationship(argument="Region", back_populates="users")
    events = relationship(argument="Event", back_populates="creator")
    attended_events = relationship(argument="EventAttendee", back_populates="attended_events")
