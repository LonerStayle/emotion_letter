from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from app.backend.config import init_firebase
import os
from firebase_admin import messaging
from app.backend.model.schema.FcmRequest import FcmRequest
from app.backend.services.user_service import (
    create_or_activate_user,
    deactivate_user,
    watch_status,
    is_active_user,
    set_bpm_user,
)
from app.backend.model.schema.StartLetterRequest import StartLetterRequest
from app.backend.model.schema.StartLetterResponse import StartLetterResponse
from app.backend.model.domain.Users import Users
from fastapi import Depends
from fastapi.staticfiles import StaticFiles
from app.backend.config import get_db
from sqlalchemy.orm import Session
from dotenv import load_dotenv
load_dotenv()
app = FastAPI()
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
init_firebase()

# @app.post("/send_push")
# async def send_push(req: FcmRequest):
#     message = messaging.Message(
#         notification=messaging.Notification(
#             title=req.title,
#             body=req.body,
#         ),
#         token=req.token,
#     )
#     try:
#         response = messaging.send(message)
#         return {"success": True, "response": response}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

@app.get('/health')
def health_check():
    return {"success": True}

@app.post("/letter/start")
def create_or_user(req: StartLetterRequest, db: Session = Depends(get_db)):
    user = create_or_activate_user(db, req.name, req.token)
    success = True
    if user is None:
        success = False

    return {"success": success}


@app.post("/letter/upload")
async def upload_image(
    name: str = Form(...), file: UploadFile = File(...), db: Session = Depends(get_db)
):  
    BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
    os.makedirs("./uploads", exist_ok=True)
    contents = await file.read()
    file_path = f"./uploads/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(contents)
            
    image_url = f"{BASE_URL}/uploads/{file.filename}"

    user = deactivate_user(db=db, name=name, image_url=image_url)
    if not user:
        return {"error": f"'{name}' 유저를 찾을 수 없습니다."}
    return {"success": True}


@app.get("/watch/status")
def get_watch_status(name: str, db: Session = Depends(get_db)):
    is_active = watch_status(db = db, name = name)
    return {"success": is_active}


@app.get("/watch/start")
def active_user(name: str, db: Session = Depends(get_db)):
    is_active = is_active_user(db = db, name=name)
    return {"success": is_active}


@app.post("/watch/send/bpm")
def send_bpm(name: str, bpm: int, db: Session = Depends(get_db)):
    set_bpm_user(db = db, bpm = bpm, name = name)
    return {"success": True}
