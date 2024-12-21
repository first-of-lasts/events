from typing import List

from sqlalchemy import String, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from events.infrastructure.adapters.database.manager import Base


class Country(Base):
    __tablename__ = "countries"

    code: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)
    #
    translations: Mapped[List["CountryTranslation"]] = relationship(
        "CountryTranslation",
        back_populates="country",
        cascade="all, delete-orphan"
    )
    # regions: Mapped[List["Region"]] = relationship("Region", back_populates="country")
    users: Mapped[List["User"]] = relationship("User", back_populates="country")


class CountryTranslation(Base):
    __tablename__ = "country_translations"
    __table_args__ = (UniqueConstraint('country_id', 'language_code', name='uix_country_language'),)

    country_id: Mapped[int] = mapped_column(Integer, ForeignKey("countries.id"), nullable=False)
    language_code: Mapped[str] = mapped_column(String(10), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    #
    country = relationship("Country", back_populates="translations")
