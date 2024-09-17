from fastapi import FastAPI, Depends, status, Response, HTTPException
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

@app.post('/create-task', status_code=status.HTTP_201_CREATED)
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

@app.get('/tasks')
def alltasks(db: Session = Depends(get_db)):
    tasks = db.query(models.Task).all()
    return tasks

# get blog by ID
@app.get('/task/{id}', status_code=status.HTTP_200_OK)
def singletask(id, response: Response, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Task with the id {id} is not available')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return{
        #     'message':f'Task with the id {id} is not available'
        # }
    return task

# delete task
@app.delete('/task/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == id)
    if not task.first():
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"Task with id {id} not found")
    task.delete(synchronize_session=False)
    db.commit()
    return {
        'message': "deleted!"
    }
    
# update task
@app.put('/task/{id}', status_code=status.HTTP_202_ACCEPTED)
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
