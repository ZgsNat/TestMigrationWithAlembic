from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from src.domain.entities.models.base import Base, TimestampMixin

class User(Base, TimestampMixin):
    __tablename__ = 'users'
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    dob = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<User(username={self.username}, email={self.email})>"
