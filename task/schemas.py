from pydantic import BaseModel
from typing import Optional


class Task(BaseModel):
    title: str
    duration: str
    completed: Optional[bool] = False

# response model
class ShowTask(BaseModel):
    # you could just return the Basemodel if you wish
    title: str
    duration: str
    completed: bool
    
    class Config():
        orm_mode = True

class UpdateTask(BaseModel):
    title: Optional[str] = None
    duration: Optional[int] = None
    completed: Optional[bool] = None

class User(BaseModel):
    name:str
    email:str
    password:str