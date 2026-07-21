from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "hello world"}
# uvicorn main:app --reload
# to test endpoints: http://127.0.0.1:8000/docs
# to end: ctrl+c