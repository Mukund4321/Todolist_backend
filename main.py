from  fastapi import FastAPI 
import uvicorn 
from models import Task

app = FastAPI()


@app.get("/")
def greet():
    return "niggas be like: Yo!"


tasks = [
    Task(id=1, task="wash clothes", status="completed"),
    Task(id=2, task="clean room", status="pending"),
    Task(id=3, task="do homework", status="pending")
]

@app.get("/task")
def get_tasks():
    return tasks

@app.get("/task/{id}")
def specific_task(id: int, task: Task):
    for task in tasks:
        if task.id == id:
            return task
    return {"message": "Task not found"}

@app.post("/add")
def create_task(task: Task):
    tasks.append(task)
    return {"message": "task appended"}

@app.patch("/task/{id}")
def update_task(id: int, updated_task: Task):
    for i, task in enumerate(tasks):
        if task.id == id:
            tasks[i] = updated_task
            return {"message": "Task updated"}
    return {"message": "Task not found"}

@app.delete("/task/{id}")
def delete_task(id: int):
    del tasks
    tasks = [task for task in tasks if task.id != id]
    return {"message": "Task deleted"}



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)