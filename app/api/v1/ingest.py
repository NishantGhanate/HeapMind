"""
Api for documents ingestion
"""
from datetime import datetime
import json
import traceback

from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.session import get_db
from app.models import FileModel, OutboxEventModel
from app.utils.files import get_save_path


router = APIRouter()


@router.post("/upload")
async def upload_doc(
        file: UploadFile = File(...),
        session: AsyncSession = Depends(get_db)
    ):
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

    try :
        # step 1: save the file
        save_path = get_save_path(filename= file.filename)
        with open(save_path, "wb") as f:
            f.write(await file.read())

        # Step 2: Persist file metadata to DB
        file_record = FileModel(
            file_name=file.filename,
            file_path=str(save_path)
        )
        session.add(file_record)
        await session.commit()
        await session.refresh(file_record)

        # Step 3: Create outbox event in DB
        event = OutboxEventModel(
            event_type="document_ingested",
            payload=json.dumps({
                "file_id": str(file_record.id),
                "file_path": file_record.file_path
            }),
            processed=False
        )
        session.add(event)
        await session.commit()

    except Exception as e:
        traceback.print_exc()
        raise e

    return JSONResponse(
        status_code=200,
        content={
            "message": "File uploaded and queued for processing",
            "file_id": file_record.id
        }
    )
