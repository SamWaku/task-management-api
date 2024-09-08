from pydantic import BaseModel
from typing import Optional


class Task(BaseModel):
    title: str
    duration: str
    # completed: Optional[bool] = False