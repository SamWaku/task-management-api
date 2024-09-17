from pydantic import BaseModel
from typing import Optional


class Task(BaseModel):
    title: str
    duration: str
    completed: Optional[bool] = False

class UpdateTask(BaseModel):
    title: Optional[str] = None
    duration: Optional[int] = None
    completed: Optional[bool] = None