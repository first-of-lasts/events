from typing import List, Optional

from sqlalchemy import String, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from events.infrastructure.adapters.database.manager import Base


class Region(Base):
    __tablename__ = "regions"

    country_id: Mapped[int] = mapped_column(Integer, ForeignKey("countries.id"), nullable=False)
    code: Mapped[str] = mapped_column(String(10), nullable=False)
    #
    translations: Mapped[List["RegionTranslation"]] = relationship(
        "RegionTranslation",
        back_populates="region",
        cascade="all, delete-orphan"
    )
    country: Mapped[Optional["Country"]] = relationship(argument="Country", back_populates="regions")
    users: Mapped[List["User"]] = relationship(argument="User", back_populates="region")


class RegionTranslation(Base):
    __tablename__ = "region_translations"
    __table_args__ = (UniqueConstraint('region_id', 'language_code', name='uix_region_language'),)

    region_id: Mapped[int] = mapped_column(Integer, ForeignKey("regions.id"), nullable=False)
    language_code: Mapped[str] = mapped_column(String(10), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    #
    region: Mapped[Region] = relationship(argument="Region", back_populates="translations")
