from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()

class OurBaseModel(BaseModel):
    class Config():
        orm_mode =True
        
# Pydantic model for input validation
class NoteCreate(OurBaseModel):
    id: int
    task: str
    
    
@app.get("/gettaskbyid/{task_id}")
async def gettask_byid(task_id : int ): #Pydantic
    return {"task_ID is " : {task_id} }


@app.post("/addtask")
async def addtask(note :  NoteCreate):
    return {
        "Id" : note.id,
        "Task" : note.task
    }

