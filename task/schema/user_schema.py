from pydantic import BaseModel

class CreateUser(BaseModel):
    id: int
    name:str
    email:str
    password: str

class User(BaseModel):
    id: int
    name:str
    email:str