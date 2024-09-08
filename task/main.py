from fastapi import FastAPI, Depends
from . import schemas, models
from .database import engine
from sqlalchemy.orm import Session

models.Base.metadata.create_all(engine)

app = FastAPI()


@app.get('/create-blog')
def create(request: schemas.Task):
    return request