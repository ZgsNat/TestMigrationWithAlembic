from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from src.domain.entities.models.base import Base, TimestampMixin
from src.domain.entities.common.enumeration.definition.taskStatus import TaskStatus  # Adjust the import path as necessary
class Task(TimestampMixin,Base):
    __tablename__ = 'tasks'
    title = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    # status = Column(String(50), nullable=False, default='pending')  # e.g., pending, in_progress, completed but better to use enum
    status = Column(Enum(TaskStatus, name="task_status"), nullable=False, default=TaskStatus.pending)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"<Task(title={self.title}, status={self.status})>"