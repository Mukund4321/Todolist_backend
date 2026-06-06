from  fastapi import FastAPI, HTTPException, Depends 
import uvicorn 
from models import Task
import database_models
from auth import hash_password, create_token, get_current_user
from database import sessionLocal, engine
from sqlalchemy.orm import Session
import auth
from fastapi.security import OAuth2PasswordRequestForm
from models import UserCreate, UserOut, Token
import models

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

@app.post("/register")
def register_user(user: models.UserCreate, db: Session = Depends(get_db)):
    hashed_password = hash_password(user.password)
    db_user = database_models.User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    return {"message": "User created"}

@app.post("/login")
def login (form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(database_models.User).filter(database_models.User.username == form.username).first()
    if not user or not auth.verify_password(form.password, user.hashed_password):
       raise HTTPException(status_code=401, detail="Wrong username or password")
    token = create_token(user.username)
    return {"access_token": token, "token_type": "bearer"}


@app.get("/")
def greet():
    return "Backend is running"


@app.get("/task")
def get_tasks(db: Session = Depends(get_db), current_user=Depends(auth.get_current_user)):
    tasks = db.query(database_models.Task).all()
    return tasks
    

@app.get("/task/{id}")
def specific_task(task_id: int, db: Session = Depends(get_db), current_user=Depends(auth.get_current_user)):
     task = db.query(database_models.Task).filter(database_models.Task.id == task_id).first()
     if task:
        return task
     return {"error": "Task not found"}

@app.post("/add")
def create_task(task: Task, db: Session = Depends(get_db), current_user=Depends(auth.get_current_user)):
    db_task = database_models.Task(id=task.id, task=task.task, status=task.status)
    db.add(db_task)
    db.commit()
    return {"message": "Task created"}

@app.patch("/task/{id}")
def update_task(id: int, updated_task: Task, db: Session = Depends(get_db), current_user=Depends(auth.get_current_user)):
    task = db.query(database_models.Task).filter(database_models.Task.id == id).first()
    if task:
        task.task = updated_task.task
        task.status = updated_task.status
        db.commit()
        return {"message": "Task updated"}
    return {"message": "Task not found"}

@app.delete("/task/{id}")
def delete_task(id: int, db: Session = Depends(get_db), current_user=Depends(auth.get_current_user)):
    task = db.query(database_models.Task).filter(database_models.Task.id == id).first()
    if task:
        db.delete(task)
        db.commit()
        return {"message": "Task deleted"}
    return {"message": "Task not found"}
  


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)