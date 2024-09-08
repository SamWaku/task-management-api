from fastapi import FastAPI
from . import schemas, models
from .database import engine
from sqlalchemy.orm import Session 

models.Base.metadata.create_all(engine)

app = FastAPI()


@app.get('/create-blog')
def create(request: schemas.Task):
    return request