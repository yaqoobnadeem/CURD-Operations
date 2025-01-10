from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from database import Base, engine

# Function to create the table
def create_table():
    Base.metadata.create_all(bind=engine)

# SQLAlchemy model for the 'notes' table
class Note(Base):
    __tablename__ = 'notes'
    
    #use SQLAlchemy's Mapped type hint from the sqlalchemy.orm module.
    Id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    task: Mapped[str] = mapped_column(String(500), nullable=False)
