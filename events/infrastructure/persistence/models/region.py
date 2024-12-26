from typing import List, Optional

from sqlalchemy import String, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from events.infrastructure.persistence.manager import Base
from events.infrastructure.persistence.config import load_supported_languages


class Region(Base):
    __tablename__ = "regions"

    for lang in load_supported_languages():
        locals()[f"name_{lang}"] = mapped_column(String(255), nullable=True)
    country_id: Mapped[int] = mapped_column(Integer, ForeignKey("countries.id"), nullable=False)
    country: Mapped[Optional["Country"]] = relationship(argument="Country", back_populates="regions")
    users: Mapped[List["User"]] = relationship(argument="User", back_populates="region")

    def get_name(self, language: str) -> str:
        return getattr(self, f"name_{language}", "")
