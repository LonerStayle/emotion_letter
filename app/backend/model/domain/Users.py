from sqlalchemy import Column, Integer, String, Boolean
from app.backend.config import Base

class Users(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    fcm_token = Column(String, unique=True)
    is_active = Column(Boolean, default=False)
    is_waiting = Column(Boolean, default=False)
    bpm = Column(Integer, nullable=True)  
    write_letter = Column(String, nullable=True)  
    image_url = Column(String, nullable=True)  
    complate_url = Column(String, nullable=True)  
    