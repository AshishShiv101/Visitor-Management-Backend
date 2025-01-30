from uuid import uuid4
from sqlalchemy import UUID, Column, String, Boolean
from db.base import ModelBase

class Visitors(ModelBase):
    
    __tablename__ = "visitors"
    
    id = Column(UUID, primary_key = True, default = uuid4)
    visitor_name = Column(String(), nullable = False)
    phno = Column(String(), nullable = False)
    email = Column(String(), nullable = False)
    
    def __repr__(self):
        return (
            f"** visitors ** "
            f"id : {self.id} "
            f"visitor_name : {self.visitor_name} "
            f"phno : {self.phno} "
            f"email : {self.email} "
            f"created_at : {self.created_at} "
            f"updated_at : {self.updated_at} "
        )