from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from events.infrastructure.persistence.manager import Base
from events.infrastructure.persistence.config import load_supported_languages


class Region(Base):
    __tablename__ = "regions"

    for lang in load_supported_languages():
        locals()[f"name_{lang}"] = mapped_column(String(255), nullable=True)
    # Foreign Keys
    country_id: Mapped[int] = mapped_column(Integer, ForeignKey("countries.id"), nullable=False)
    # Relationships
    country = relationship(argument="Country", back_populates="regions")
    users = relationship(argument="User", back_populates="region")
    events = relationship(argument="Event", back_populates="region")

    def get_name(self, language: str) -> str:
        return getattr(self, f"name_{language}", "")
