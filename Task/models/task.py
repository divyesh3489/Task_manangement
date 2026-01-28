from db.base import Base
from sqlalchemy import String, Boolean, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column
import enum

class StatusEnum(str, enum.Enum):
    """
    Enum for Task Statuses
    """
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    HOLD = "hold"

class PriorityEnum(str, enum.Enum):
    """
    Enum for Task Priority Levels
    """
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"



class Task(Base):
    """
    Task model representing a task in the task management system.
    """
    __tablename__ = "tasks"

    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    status: Mapped[StatusEnum] = mapped_column(Enum(StatusEnum), default=StatusEnum.PENDING)
    priority: Mapped[PriorityEnum] = mapped_column(Enum(PriorityEnum), default=PriorityEnum.MEDIUM)
    due_date: Mapped[DateTime | None] = mapped_column(DateTime, nullable=True)
