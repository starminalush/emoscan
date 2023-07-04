from sqlalchemy import ARRAY, Column, DateTime, Integer, Text
from sqlalchemy.dialects.postgresql import UUID

from core.db.database import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    track_id = Column(Integer, comment="TrackID aka studentID")
    datetime = Column(DateTime, comment="Event datetime")
    emotion = Column(Text, comment="Face emotion")
    bbox = Column(ARRAY(Integer), comment="Face bbox")
    image_uuid = Column(UUID(as_uuid=True), comment="Image name in S3")
    task_id = Column(UUID(as_uuid=True), comment="TaskID aka lessonID")
