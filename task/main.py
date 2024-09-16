from fastapi import FastAPI
from . import schemas, models
from .database import engine

models.Base.metadata.create_all(engine)

app = FastAPI()

@app.get('/')
def indexmain():
    return "Connected!"

@app.get('/create-blog')
def create(request: schemas.Task):
    return request