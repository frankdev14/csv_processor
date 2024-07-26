import shutil
from fastapi import FastAPI, UploadFile, File, BackgroundTasks, Depends
from sqlalchemy.orm import Session
from database.database import SessionLocal
from database.models import Task
from tasks.tasks import process_csv_task

app = FastAPI()

def get_session():
    """
    Method for the DB Session.

    Yields:
        Session: A SQLAlchemy database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def save_upload_file(upload_file: UploadFile, destination: str) -> None:
    """
    Saves the uploaded file on disk.

    Args:
        upload_file (UploadFile): The file to be saved.
        destination (str): The path where the file will be saved.

    Returns:
        None
    """
    with open(destination, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)

@app.post("/upload_csv/")
async def upload_csv(background_tasks: BackgroundTasks, file: UploadFile = \
    File(...), db: Session = Depends(get_session)):
    """
    Handles the upload of a CSV file, saves it to a temporary location,
    and schedules a background task to process the file.

    Args:
        background_tasks (BackgroundTasks): FastAPI BackgroundTasks instance.
        file (UploadFile): The uploaded CSV file.
        db (Session): The database session.

    Returns:
        dict: A dictionary containing the task ID.
    """
    task = Task(file_name=file.filename, is_finished=False)
    db.add(task)
    db.commit()
    db.refresh(task)

    input_file_path = f"processors/tmp/{file.filename}"
    output_file_path = f"../output_data/processed_{file.filename}"

    save_upload_file(file, input_file_path)

    background_tasks.add_task(process_csv_task, task.id, input_file_path, \
        output_file_path)

    return {"task_id": task.id}

@app.get("/task_status/{task_id}")
def get_task_status(task_id: int, db: Session = Depends(get_session)):
    """
    Retrieves the status of a background task by ID.

    Args:
        task_id (int): The ID of the task.
        db (Session): The database session.

    Returns:
        dict: A dictionary containing the task ID, its completion status,
        and the output file path if available.
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        return {"status": "Task not found"}

    return {
        "task_id": task.id,
        "is_finished": task.is_finished,
        "output_file": task.output_file
    }
