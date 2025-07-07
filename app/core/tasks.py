"""
Add backround / celery task here
"""
# app/worker/tasks.py

import logging
from pathlib import Path

from celery import shared_task

from app.embeddings.emedder import Embedder
from app.utils.document_parser import DocumentParser
from app.vector_store.qdrant_db import qdrant_store


logger = logging.getLogger(__name__)

@shared_task(name="app.core.tasks.process_document", bind=True)
def process_document(self, event_id: str, payload: dict, event_type: str):
    """
    Celery task to process uploaded document files.
    Flow: parse_file(path) → embed_vector(file_id) → generate_quiz(file_id)

    Args:
        event_id (str): Unique ID of the outbox event.
        payload (dict): JSON-serializable dict containing file metadata.
        event_type (str): Type of event, e.g., "document_ingested".

    """
    try:
        file_id = payload["file_id"]
        file_path = Path(payload["file_path"])
        logger.info(f"[{event_type}] Processing file {file_id} at {file_path}")

        # Step 1: Parse document
        words = DocumentParser.parse_document(file_path= file_path)

        # Step 2: Embed Chunks
        embeddings = Embedder.embed_texts(texts= words)

        metadata = {
            "file_id": file_id,
            "file_path": str(file_path),
            "file_name": file_path.name
        }

        # Step 3: Store em
        qdrant_store.store(
            embeddings=embeddings,
            chunks=words,
            metadata=metadata,
            collection_name='documents'
        )

    except Exception as exc:
        logger.error(f"Failed to process event {event_id}: {exc}", exc_info=True)
        raise self.retry(exc=exc, countdown=10, max_retries=3)
