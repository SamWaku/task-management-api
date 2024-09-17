from fastapi import FastAPI, Depends
from . import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session

models.Base.metadata.create_all(engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/')
def indexmain():
    return "Connected!"

@app.post('/create-task')
def create(request: schemas.Task, db: Session = Depends(get_db)):
    new_task = models.Task(title=request.title, duration=request.duration)
    db.add(new_task)
    db.commit()
    db.refresh
    return new_task