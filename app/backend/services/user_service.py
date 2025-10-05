from sqlalchemy.orm import Session
from app.backend.model.domain.Users import Users

def create_or_activate_user(db: Session, name: str, fcm_token: str):

    existing_user = db.query(Users).filter(Users.name == name.strip()).first()
    
    if existing_user:
        existing_user.is_waiting = True
        db.commit()
        db.refresh(existing_user)
        return existing_user
    

    new_user = Users(
        name=name,
        fcm_token=fcm_token,
        is_waiting=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def is_active_user(db: Session, name: str):
    if not name:
        return False

    existing_user = db.query(Users).filter(Users.name == name.strip()).first()

    if not existing_user:
        return False

    if not existing_user.is_active:
        existing_user.is_active = True
        db.commit()
        db.refresh(existing_user)

    return True

def deactivate_user(db: Session, name: str, image_url: str = None):
    """유저를 찾아 is_active=False로 만들고, 이미지 경로도 업데이트"""
    user = db.query(Users).filter(Users.name == name.strip()).first()
    if not user:
        return None

    user.is_active = False
    if image_url:
        user.image_url = image_url  
        # 윤재님 !!! ) 여기서 OCR 써갓고 편지 내용 전달 저장 
        user.write_letter = 'adasd'
    
    db.commit()
    db.refresh(user)
    return user

def set_bpm_user(db:Session, bpm:int, name:str):
    user = db.query(Users).filter(Users.name == name.strip()).first()
    user.bpm = bpm
    db.commit()
    db.refresh(user)
    
    # 여기서 AI 모델 사용 (write_letter +  bpm  = 글내용 합침)
    user.bpm = bpm
    user.write_letter
    
    # AI. 모델 사용후 최종 생성된 편지 이미지 저장 (임시로 image_url 넣음)
    user.complate_url = user.image_url
    db.commit()
    db.refresh(user)

def watch_status(db: Session, name: str):
    return db.query(Users).filter(Users.name == name.strip()).first().is_active