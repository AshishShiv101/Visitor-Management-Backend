from uuid import uuid4
from sqlalchemy import UUID, Column, String, Boolean
from db.base import ModelBase

class Meetings(ModelBase):
    
    __tablename__ = "meetings"
    
    id = Column(UUID, primary_key = True, default = uuid4)
    visitor_id = Column(String(), nullable = False)
    user_id = Column(String(), nullable = False)
    meeting_remarks = Column(String(), nullable = False)
    meeting_status_id = Column(UUID, nullable = False)
    meeting_time = Column(Boolean, default = True)
    
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