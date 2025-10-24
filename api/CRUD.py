from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()

class Task(BaseModel):
    id: int
    name: str
    done: bool = False

tasks = []

@app.post("/tasks") 
def create_task(task: Task):
    tasks.append(task)
    return task 


@app.get("/tasks")
def read_task(): 
    return tasks

@app.put ("/tasks/{task_id}")
def update_task(task_id: int, done: bool): 
    for task in tasks: 
        if task.id == task_id: 
            task.done = done 
            return task 
        else: 
            return {"error": "404 not found"}  



@app.delete("/tasks/{task_id}")  
def delete_task(task_id: int): 
    for task in tasks: 
        if task.id == task_id: 
            tasks.remove(task) 
            return {"message": "Task deleted"} 
        else:
            return {"error": "404 not found"} 


