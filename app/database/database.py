from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

# URL for the SQLite database
SQLALCHEMY_DATABASE_URL = "sqlite:///./database/bmat_tasks.db"

# Create an SQLAlchemy engine instance
engine = create_engine(SQLALCHEMY_DATABASE_URL, \
    connect_args={"check_same_thread": False})

# Create a session factory for creating new database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all tables in the database
Base.metadata.create_all(bind=engine)
