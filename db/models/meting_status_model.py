from uuid import uuid4
from sqlalchemy import UUID, Column, Enum
from db.utils.db_enums import MeetingsStatusEnum
from db.base import ModelBase

class Roles(ModelBase):
    
    __tablename__ = "meeting_status"
    
    id = Column(UUID, primary_key = True, default = uuid4)
    meeting_status = Column(Enum(MeetingsStatusEnum), nullable=False)
    
    def __repr__(self):
        return (
            f"** roles ** "
            f"id : {self.id} "
            f"meeting_status : {self.meeting_status.value} "
            f"created_at : {self.created_at} "
            f"updated_at : {self.updated_at} "
        )