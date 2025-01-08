from sqlalchemy import String,Integer,Column

from database import Base,engine


def create_table():
    Base.metadata.create_all(bind = engine)
    
    

# SQLAlchemy model for `notes` table
class Note(Base):
    __tablename__ = 'notes'
    Id = Column(Integer, primary_key=True, index=True)
    task = Column(String(500), nullable=False)

