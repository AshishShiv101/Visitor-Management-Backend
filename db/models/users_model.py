from uuid import uuid4
from sqlalchemy import UUID, Column, String, Boolean
from db.base import ModelBase

class Users(ModelBase):
    
    __tablename__ = "users"
    
    id = Column(UUID, primary_key = True, default = uuid4)
    user_name = Column(String(), nullable = False)
    phno = Column(String(), nullable = False)
    password = Column(String(), nullable = False)
    role_id = Column(UUID, nullable = False)
    is_active = Column(Boolean, nullable = False, default = True)
    
    def __repr__(self):
        return (
            f"** users ** "
            f"id : {self.id} "
            f"user_name : {self.user_name} "
            f"phno : {self.phno} "
            f"password : {self.password} "
            f"role_id : {self.role_id} "
            f"is_active : {self.is_active} "
            f"created_at : {self.created_at} "
            f"updated_at : {self.updated_at} "
        )