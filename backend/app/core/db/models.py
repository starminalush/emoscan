from sqlalchemy import Column, DateTime, Integer, Text, ARRAY
from sqlalchemy.dialects.postgresql import UUID

from core.db.database import Base


class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, autoincrement=True)
    track_id = Column(Integer)
    datetime = Column(DateTime)
    emotion = Column(Text)
    bbox = Column(ARRAY(Integer))
    image_uuid = Column(UUID(as_uuid=True))
    task_id = Column(UUID(as_uuid=True))
