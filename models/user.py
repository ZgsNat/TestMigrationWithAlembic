from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from models.base import Base, TimestampMixin

class User(Base, TimestampMixin):
    __tablename__ = 'users'
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    
    # Uncomment if you want to add more fields
    # age = Column(Integer, nullable=True)
    # address = Column(String(255), nullable=True)
    
    def __repr__(self):
        return f"<User(username={self.username}, email={self.email})>"
