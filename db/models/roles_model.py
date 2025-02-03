from uuid import uuid4
from sqlalchemy import UUID, Column, Enum
from db.utils.db_enums import RoleEnum
from db.base import ModelBase

class Roles(ModelBase):
    
    __tablename__ = "roles"
    
    id = Column(UUID, primary_key = True, default = uuid4)
    role = Column(Enum(RoleEnum), nullable=False)
    
    def __repr__(self):
        return (
            f"** roles ** "
            f"id : {self.id} "
            f"role : {self.role.value} "
            f"created_at : {self.created_at} "
            f"updated_at : {self.updated_at} "
        )