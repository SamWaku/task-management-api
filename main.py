# imports
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import uvicorn 

app = FastAPI()

class Task(BaseModel): 
    title: str
    duration: str
    completed: Optional[bool] = False

# some methods
# rest functionality
@app.get('/task')
def index(limit=10, completed: Optional[bool] = False, sort: Optional[str] = None):
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
def create_task(task: Task):
    return {"data": f"Task of duration: {task.duration}, is created with title {task.title}"}


@app.get('/get-task/{id}')
def task_by_id(id):
    return {"data": id}


# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=5000)
