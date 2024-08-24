# imports
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Task(BaseModel): 
    title: str
    duration: str
    completed: Optional[bool]

# some methods
# rest functionality
@app.get('/task')
def index(limit=10, completed: bool = True, sort: Optional[str] = None):
    # 10 completed tasks
    if completed: 
        return {'data': f'{limit} completed tasks from the db'}
    else:
        return{'data': f'{limit} tasks from the db'}

# about
@app.get('/about')
def about():
    return {"data":{"title":"Some Title"}}



@app.post('/create-task')
def create_task(request: Task):
    return request
    return {"data": {"Task is created"}}


@app.get('/get-task/{id}')
def task_by_id(id):
    return {"data": id}