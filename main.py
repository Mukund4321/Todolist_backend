from  fastapi import FastAPI, HTTPException, Depends 
import uvicorn 
from models import Task
import database_models
from database import sessionLocal, engine
from sqlalchemy.orm import Session

database_models.base.metadata.create_all(bind=engine)

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

tasks = [
    Task(id=1, task="do homework", status="pending"),
    Task(id=2, task="go to gym", status="pending"),
    Task(id=3, task="buy groceries", status="pending")
]


def init_db():
    db = sessionLocal()
    exisiting_tasks = db.query(database_models.Task).count()

    if exisiting_tasks == 0:
        for Task in tasks:
            db_task = database_models.Task(id=Task.id, task=Task.task, status=Task.status)
            db.add(db_task)
    db.commit()
    print("Database initialized with sample tasks")
    db.close()

init_db()


app = FastAPI()


@app.get("/")
def greet():
    return "Backend is running"




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