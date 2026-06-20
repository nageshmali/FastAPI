from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://127.0.0.1:5500"],
    allow_methods = ["*"],
    allow_headers = ["*"],
)

@app.get("/message")
def get_message():
    return {"message" : "Hello from the backend"}