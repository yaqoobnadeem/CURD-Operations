from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine

# Database connection URL
url = "postgresql+psycopg2://postgres:0000@localhost/postgres"

# Create the engine
engine = create_engine(url , echo= True)

# Base class for ORM models
Base = declarative_base()

# Session factory
SessionLocal = sessionmaker(bind=engine)
