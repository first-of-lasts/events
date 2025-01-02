import enum
from datetime import datetime
from sqlalchemy import Enum, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from events.infrastructure.persistence.manager import Base


class AttendanceStatus(enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class EventAttendee(Base):
    __tablename__ = "event_attendees"

    status: Mapped[AttendanceStatus] = mapped_column(
        Enum(AttendanceStatus),
        default=AttendanceStatus.pending,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    # Foreign Keys
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    # Relationships
    attendees = relationship(argument="Event", back_populates="attendees")
    attended_events = relationship(argument="User", back_populates="attended_events")
