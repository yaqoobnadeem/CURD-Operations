from pydantic import BaseModel

class OurBaseModel(BaseModel):
    class Config():
        orm_mode = True  # To work with SQLAlchemy models and Pydantic models seamlessly

# Pydantic model for input validation when creating a new task
class NoteCreate(OurBaseModel):
    Id : int  # Task ID (mapped to the database column 'ID')
    task: str  # Task description
