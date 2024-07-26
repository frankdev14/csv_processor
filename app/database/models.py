from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Task(Base):
    """
    SQLAlchemy model representing a task that processes an uploaded file.

    Attributes:
        __tablename__ (str): The name of the table in the database.
        id (Column): The unique identifier for the task (primary key).
        file_name (Column): The name of the file associated with the task.
        is_finished (Column): A boolean flag indicating if the task is completed.
        output_file (Column): The path to the output file after processing, if any.
    """
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, index=True)
    is_finished = Column(Boolean, default=False)
    output_file = Column(String, nullable=True)
