from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from events.infrastructure.persistence.manager import Base
from events.infrastructure.persistence.config import load_supported_languages


class Country(Base):
    __tablename__ = "countries"

    for lang in load_supported_languages():
        locals()[f"name_{lang}"] = mapped_column(String(255), nullable=True)
    code: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)
    # Relationships
    users = relationship("User", back_populates="country")
    regions = relationship("Region", back_populates="country")
    events = relationship("Event", back_populates="country")

    def get_name(self, language: str) -> str:
        return getattr(self, f"name_{language}", "")
