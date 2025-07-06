"""
Add backround / celery task here
"""
# app/worker/tasks.py

import logging

from celery import shared_task


logger = logging.getLogger(__name__)

@shared_task(name="app.core.tasks.process_document", bind=True)
def process_document(self, event_id: str, payload: dict, event_type: str):
    """
    Celery task to process uploaded document files.

    Args:
        event_id (str): Unique ID of the outbox event.
        payload (dict): JSON-serializable dict containing file metadata.
        event_type (str): Type of event, e.g., "document_ingested".
    """
    try:
        file_id = payload["file_id"]
        path = payload["path"]
        logger.info(f"[{event_type}] Processing file {file_id} at {path}")

        # TODO: parse → embed → store → generate quizzes
        # e.g., parse_file(path) → embed_vector(file_id) → generate_quiz(file_id)

    except Exception as exc:
        logger.error(f"Failed to process event {event_id}: {exc}", exc_info=True)
        raise self.retry(exc=exc, countdown=10, max_retries=3)
