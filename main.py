# imports
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# some methods

# rest functionality
@app.get('/tasks')
def index():
    return {
        'data':{
            "name":"Finish task"
        }
    }

# about
@app.get('/about')
def about():
    return {"data":{"title":"Some Title"}}

class Task(BaseModel): 
    pass

@app.post('/task')
def create_task(request: Task):
    return request
    return {"data": {"Task is created"}}


@app.get()