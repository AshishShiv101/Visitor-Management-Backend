import enum

class RoleEnum(enum.Enum):
    ADMIN = "ADMIN"
    USER = "USER"
    GUEST = "GUEST"

class MeetingsStatusEnum(enum.Enum):
    PENDING = "PENDING"
    REJECTED = "REJECTED"
    APPROVED = "APPROVED"
    COMPLETED = "COMPLETED"