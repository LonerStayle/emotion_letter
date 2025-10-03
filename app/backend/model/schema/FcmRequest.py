from pydantic import BaseModel
class FcmRequest(BaseModel):
    token: str
    title: str
    body: str