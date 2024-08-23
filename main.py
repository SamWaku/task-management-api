# imports
from fastapi import FastAPI

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


@app.post('/task')
def create_task():
    return {"data": {"Task is created"}}