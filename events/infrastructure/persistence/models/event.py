from datetime import datetime
from sqlalchemy import String, ForeignKey, DateTime, func, Boolean, \
    Integer, Column, UniqueConstraint, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from events.infrastructure.persistence.manager import Base
from events.infrastructure.persistence.config import load_supported_languages


event_event_category = Table(
    "event_event_category",
    Base.metadata,
    Column("event_id", Integer, ForeignKey("events.id", ondelete="CASCADE"), primary_key=True, nullable=False),
    Column("event_category_id", Integer, ForeignKey("event_categories.id", ondelete="CASCADE"), primary_key=True, nullable=False)
)


class EventCategory(Base):
    __tablename__ = "event_categories"
    __table_args__ = (
        UniqueConstraint("sort_order", name="_sort_order_uc"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, )
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, )
    for lang in load_supported_languages():
        locals()[f"name_{lang}"] = mapped_column(String(255), nullable=True)
    # Relationships
    events: Mapped[list["Event"]] = relationship(
        "Event",
        secondary=event_event_category,
        back_populates="categories",
        order_by="EventCategory.sort_order"
    )

    def get_name(self, language: str) -> str:
        return getattr(self, f"name_{language}", "")


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(2048), nullable=False)
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    ends_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    is_occurred: Mapped[bool] = mapped_column(Boolean, default=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    #
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    # Foreign Keys
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    country_id: Mapped[int] = mapped_column(ForeignKey("countries.id"), nullable=False)
    region_id: Mapped[int] = mapped_column(ForeignKey("regions.id"), nullable=True)
    # Relationships
    categories: Mapped[list["EventCategory"]] = relationship(
        "EventCategory",
        secondary=event_event_category,
        back_populates="events",
        order_by="EventCategory.sort_order"
    )
    #
    creator = relationship(argument="User", back_populates="events")
    country = relationship(argument="Country", back_populates="events")
    region = relationship(argument="Region", back_populates="events")
    # attendees = relationship(argument="Attendee", back_populates="attendees")
