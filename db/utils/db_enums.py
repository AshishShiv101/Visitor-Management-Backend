import enum

class RoleEnum(enum.Enum):
    ADMIN = "ADMIN"
    SECURITY = "SECURITY"

class MeetingsStatusEnum(enum.Enum):
    PENDING = "PENDING"
    REJECTED = "REJECTED"
    APPROVED = "APPROVED"
    COMPLETED = "COMPLETED"