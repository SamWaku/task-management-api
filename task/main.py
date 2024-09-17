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
    new_task = models.Task(title=request.title, duration=request.duration, completed=request.completed)
    db.add(new_task)
    db.commit()
    db.refresh
    return new_task

@app.get('/tasks')
def alltasks(db: Session = Depends(get_db)):
    tasks = db.query(models.Task).all()
    return tasks

# get blog by ID
@app.get('/task/{id}')
def singletask(id, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == id).first()
    return task