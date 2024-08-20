# imports
from fastapi import FastAPI

app = FastAPI()

# some methods

# rest functionality
@app.get('/')
def index():
    return {
        'data':{
            "name":"Sam"
        }
    }