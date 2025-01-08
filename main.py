from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from database import SessionLocal
from models import Note

app = FastAPI()  # Initialize the FastAPI application

db = SessionLocal()  # Create a database session

class OurBaseModel(BaseModel):
    class Config():
        orm_mode = True  # To work with SQLAlchemy models and Pydantic models seamlessly

# Pydantic model for input validation when creating a new task
class NoteCreate(OurBaseModel):
    Id : int  # Task ID (mapped to the database column 'ID')
    task: str  # Task description
    
# Endpoint to fetch a specific task by its ID
@app.get("/gettaskbyid/{task_id}")
async def gettask_byid(task_id: int): 
    return {"task_ID is ": task_id}  # Return the task ID as a response

# Endpoint to get all tasks from the database, returning them as a list of Pydantic models
@app.get("/getalltask", response_model=list[NoteCreate], status_code=status.HTTP_200_OK)
def getalltask():
    alltask = db.query(Note).all()  # Query all tasks from the database
    return alltask  # Return the list of tasks

# Endpoint to add a new task to the database
@app.post("/addtask/", response_model=NoteCreate, status_code=status.HTTP_200_OK)
async def addtasks(note: NoteCreate):
    # Create a new task instance using the incoming data
    newtask = Note(Id=note.Id, task=note.task)  # Use note.ID here to get the ID from the request body
    
    # Check if a task with the same ID already exists
    find_task = db.query(Note).filter(Note.Id == note.Id).first()  # Compare against the database column 'ID'
    
    if find_task is not None:  # If the task exists, raise an exception
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Task with this ID already exists")
    
    # Add the new task to the database and commit it
    db.add(newtask)
    db.commit()
    db.refresh(newtask)  # Refresh the task to get the updated data (e.g., ID from DB)
    
    return newtask  # Return the created task

# Endpoint to update an existing task by its ID
@app.put("/updatetask/{ID}", response_model=NoteCreate, status_code=status.HTTP_200_OK)
def updatetask(Id: int, note: NoteCreate):
    # Find the task by ID
    find_task = db.query(Note).filter(Note.Id == note.Id).first()  # Use Note.ID for the database column
    
    if find_task is None:  # If the task doesn't exist, raise a 404 error
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task with this ID does not exist")

    # Update the task's details
    find_task.task = note.task  # Update the task description

    # Commit the changes to the database
    db.commit()
    db.refresh(find_task)  # Ensure that the task has been updated in the database
    
    return find_task  # Return the updated task

# Endpoint to delete a task by its ID
@app.delete("/deletetask", response_model=NoteCreate, status_code=200)
async def deleteperson(Id: int, note: NoteCreate):
    # Find the task by ID
    find_task = db.query(Note).filter(Note.Id == note.Id).first()  # Use Note.ID for the database column
    
    if find_task is None:  # If the task doesn't exist, raise a 404 error
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task with this ID does not exist")
    
    db.delete(find_task)  # Delete the found task
    db.commit()  # Commit the changes to the database
    
    return find_task  # Return the deleted task details (optional, for confirmation)
