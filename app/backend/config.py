import firebase_admin
from firebase_admin import credentials


def init_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate("service_account_key.json")
        firebase_admin.initialize_app(cred)
        
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
DATABASE_URL = "postgresql+psycopg2://seobi:6769@localhost:5432/emotion_letter"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()