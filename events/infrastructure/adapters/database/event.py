# from infrastructure.adapters.database.manager import Base
#
#
# class Event(Base):
#     __tablename__ = "events"
#
#     title = ""
#     description = ""
#     organizer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
#     organizer = relationship("User", back_populates="created_events")
