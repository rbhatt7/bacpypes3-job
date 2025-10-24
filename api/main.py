from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
@app.get("/greet")
def read_greet():
    return {"Hello Bob"}
@app.put("/greet")
def update_greet():
    return {"something to be added:"}