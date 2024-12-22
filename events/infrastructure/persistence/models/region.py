# from typing import List, Optional
#
# from sqlalchemy import String, Integer, ForeignKey, UniqueConstraint
# from sqlalchemy.orm import Mapped, mapped_column, relationship
#
# from events.infrastructure.adapters.persistence.manager import Base
#
#
# class Region(Base):
#     __tablename__ = "regions"
#
#     for lang in Config.app.supported_languages:
#         locals()[f"name_{lang}"] = mapped_column(String(255), nullable=True)
#     country_id: Mapped[int] = mapped_column(Integer, ForeignKey("countries.id"), nullable=False)
#     code: Mapped[str] = mapped_column(String(10), nullable=False)
#     #
#     country: Mapped[Optional["Country"]] = relationship(argument="Country", back_populates="regions")
#     users: Mapped[List["User"]] = relationship(argument="User", back_populates="region")

