"""
Api for documents ingestion
"""

from fastapi import APIRouter, File, UploadFile

from utils.files import get_save_path

router = APIRouter()


@router.post("/upload")
async def upload_doc(file: UploadFile = File(...)):
    """

    Upload PDF → store in DB → send message to RabbitMQ queue:
    {
        "file_id": "123",
        "path": "/data/documents/abc.pdf"
    }

    Worker:
    - Waits on queue
    - Fetches file
    - Parses → splits → embeds → saves vectors → generates quizzes
    """
    save_path = get_save_path(filename= file.filename)
    with open(save_path, "wb") as f:
        f.write(await file.read())
    # process_file_task.delay(save_path)  # Send to RabbitMQ
    return {"status": "queued"}
