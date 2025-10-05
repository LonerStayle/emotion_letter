from pydantic import BaseModel

class StatusResponse(BaseModel):
    isStarted: bool