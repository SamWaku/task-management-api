from fastapi import FastAPI
from . import schemas

app = FastAPI()


@app.get('/create-blog')
def create(request: schemas.Task):
    return request