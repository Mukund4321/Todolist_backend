from pydantic import BaseModel

class Task(BaseModel):
    id: int
    task: str
    status: str