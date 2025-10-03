from sqlalchemy import Column, Integer, String
from app.backend.config import Base

class Users(Base):
    __tablename__="users"
    __table_args__ = {"schema": "public"} 
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    fcm_token = Column(String, unique=True)
    
    