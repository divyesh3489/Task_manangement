from pydantic import BaseModel,validator
from enum import Enum
from datetime import datetime

class StatusEnum(str, Enum):
    """
    Enum for Task Statuses
    """
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    HOLD = "hold"

class PriorityEnum(str, Enum):
    """
    Enum for Task Priority Levels
    """
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class TaskBase(BaseModel):
    """
    Base schema for Task 
    """
    id: int
    title: str
    description: str | None = None
    status : StatusEnum = StatusEnum.PENDING
    priority: PriorityEnum = PriorityEnum.MEDIUM
    due_date: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    
class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    status : StatusEnum = StatusEnum.PENDING
    priority: PriorityEnum = PriorityEnum.MEDIUM
    due_date: datetime | None = None
    @validator("title", pre=True, always=True)
    def validate_title(cls, value):
        if not value or value.strip() == "":
            raise ValueError("title cannot be Empty")
        return value

class TaskUpdate(BaseModel):
    """
    Schema for updating a Task
    """
    title: str | None = None
    description: str | None = None

    status : StatusEnum | None = None
    priority: PriorityEnum | None = None
    due_date: datetime | None = None

    @validator("title", pre=True, always=True)
    def validate_title(cls, value):
        if value is not None and value.strip() == "":
            raise ValueError("title cannot be Empty")
        return value

    
class TaskPriporityUpdate(BaseModel):
    """
    Schema for updating Task Priority
    """
    priority: PriorityEnum
    @validator("priority", pre=True, always=True)
    def validate_priority(cls, value):
        if value is None:
            raise ValueError("priority cannot be Empty")
        return value

class TaskStatusUpdate(BaseModel):
    """
    Schema for updating Task Status
    """
    status: StatusEnum
    @validator("status", pre=True, always=True)
    def validate_status(cls, value):
        if value is None:
            raise ValueError("status cannot be Empty")
        return value

