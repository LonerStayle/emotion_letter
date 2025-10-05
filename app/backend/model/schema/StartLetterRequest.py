from pydantic import BaseModel

class StartLetterRequest(BaseModel):
    token:str
    name:str
    