from database.database import SessionLocal
from database.models import Task
from processors.csv_processor import CSVProcessor
import asyncio
import os

async def process_csv_task(task_id, input_file, output_file):
    """
    Processes a CSV file asynchronously and updates the task status in the database.

    This function simulates a long processing time if `DEBUG_MODE` is enabled,
    processes the CSV file using the `CSVProcessor`, and then updates the task status
    in the database to indicate completion. The output file path is also recorded.

    Args:
        task_id (int): ID of the task to be updated in the database.
        input_file (str): The path to the input CSV file that needs to be processed.
        output_file (str): The path where the processed output file will be saved.

    Returns:
        None
    """
    session = SessionLocal()
    try:
        if os.getenv("DEBUG_MODE") == "true":
            print("Debug mode is enabled. Simulating long processing time...")
            await asyncio.sleep(30)  # Simulate a 10-second delay

        processor = CSVProcessor(input_file, output_file, chunk_size=1000)
        processor.process(tmp=True)
        task = session.query(Task).filter(Task.id == task_id).first()
        task.is_finished = True
        task.output_file = os.path.abspath(output_file)
        session.commit()
    finally:
        session.close()
