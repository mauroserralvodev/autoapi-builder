from fastapi import FastAPI, Request
from api_generator import generate_api
from storage import data_store

app = FastAPI()
generate_api(app, data_store)

@app.get("/")
def read_root():
    return {"message": "AutoAPI Builder is running."}
