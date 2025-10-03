from sqlalchemy.orm import Session
from app.backend.model.domain.Users import Users

def create_user_test(db:Session,fcm_token:str):
    db_user = Users(name="이진섭",fcm_token=fcm_token)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user