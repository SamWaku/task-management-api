from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import List
from .controllers.users.auth import hashing
from .schema.user_schema import User


models.Base.metadata.create_all(engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# index page
@app.get('/')
def indexmain():
    return "Connected!"

# create task
@app.post('/create-task', status_code=status.HTTP_201_CREATED, tags=['tasks'])
def create(request: schemas.Task, db: Session = Depends(get_db)):
    new_task = models.Task(title=request.title, duration=request.duration, completed=request.completed)
    db.add(new_task)
    db.commit()
    db.refresh
    return {
        "title": new_task.title,
        "duration": new_task.duration,
        "completed": new_task.completed
    }

# get all tasks
@app.get('/tasks', status_code=status.HTTP_200_OK, response_model=List[schemas.ShowTask], tags=['tasks']) #getting a List, so specify
def alltasks(db: Session = Depends(get_db)):
    tasks = db.query(models.Task).all()
    if not tasks:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No Task records found")
    return tasks

# get blog by ID
@app.get('/task/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowTask, tags=['tasks'])
def singletask(id, response: Response, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Task with the id {id} is not available')
    return task

# delete task
@app.delete('/task/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['tasks'])
def destroy(id, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == id)
    if not task.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id {id} not found")
    task.delete(synchronize_session=False)
    db.commit()
    return {
        'message': "deleted!"
    }
    
# update task
@app.put('/task/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['tasks'])
def update(id: int, request: schemas.UpdateTask, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == id)
    
    if not task.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id {id} not found")
    
    # Only update the fields that are present in the request
    update_data = request.dict(exclude_unset=True)  # `exclude_unset=True` ensures we only update provided fields
    
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields provided for update")

    task.update(update_data)
    db.commit()
    
    return {'detail': 'Task updated'}


@app.post('/create-user', response_model=User, tags=['users'])
def create_user(request: User, db: Session = Depends(get_db)):
    new_user = models.User(
        name=request.name,
        email=request.email,
        password=hashing.Hash.bcrypt(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/user/{id}', response_model=User, tags=['users'])
def get_user(id:int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with the id {id} is not found")
    
    return user

@app.get('/users', status_code=status.HTTP_200_OK, response_model=List[User], tags=['users']) #getting a List, so specify
def allusers(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No User records found")
    return users