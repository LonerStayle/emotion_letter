from fastapi import FastAPI, HTTPException
from app.backend.config import init_firebase

from firebase_admin import messaging
from app.backend.model.schema.FcmRequest import FcmRequest
from app.backend.services.user_service import create_user_test
from app.backend.config import SessionLocal

app = FastAPI()
init_firebase()

@app.post("/send_push")
async def send_push(req:FcmRequest):
    message = messaging.Message(
        notification=messaging.Notification(
            title=req.title,
            body=req.body,
        ),
        token=req.token,
    )
    try:
        response = messaging.send(message)
        return {"success": True, "response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

db = SessionLocal()    
@app.post("/create_user")
def test_create_user(token:str):
    create_user_test(db,token)
    return {"success":True}
    
    
