from pydantic import BaseModel

class TextRequest(BaseModel):
    text: str

class QueueRequest(BaseModel):
    text: str