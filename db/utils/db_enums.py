import enum

class RoleEnum(enum.Enum):
    ADMIN = "ADMIN"
    SECURITY = "SECURITY"
    ATTENDEE = "ATTENDEE"

class MeetingsStatusEnum(enum.Enum):
    PENDING = "PENDING"
    REJECTED = "REJECTED"
    APPROVED = "APPROVED"
    COMPLETED = "COMPLETED"
    MISSED = "MISSED"