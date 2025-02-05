from uuid import uuid4
from sqlalchemy import UUID, Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from db.models.meting_status_model import MeetingStatus
from db.base import ModelBase
from db.base import db
from db.utils.db_enums import MeetingsStatusEnum

class Meetings(ModelBase):
    
    __tablename__ = "meetings"
    
    id = Column(UUID, primary_key = True, default = uuid4)
    visitor_id = Column(UUID, nullable = False)
    user_id = Column(UUID, nullable = False)
    meeting_remarks = Column(String(), nullable = True)
    meeting_status_id = Column(UUID, ForeignKey("meeting_status.id"), nullable = False, default = None)
    meeting_time = Column(DateTime, nullable = False)
    
    meeting_status = relationship("MeetingStatus") 

    def __init__(self, **kwargs):
        if "meeting_status_id" not in kwargs:
            pending_status = db.session.query(MeetingStatus).filter_by(meeting_status=MeetingsStatusEnum.PENDING).first()
            kwargs["meeting_status_id"] = pending_status.id if pending_status else None

        super().__init__(**kwargs)

    def __repr__(self):
        return (
            f"** meetings ** "
            f"id : {self.id} "
            f"visitor_id : {self.visitor_id} "
            f"user_id : {self.user_id} "
            f"meeting_time : {self.meeting_time} "
            f"meeting_status_id : {self.meeting_status_id} "
            f"meeting_remarks : {self.meeting_remarks} "
            f"created_at : {self.created_at} "
            f"updated_at : {self.updated_at} "
        )