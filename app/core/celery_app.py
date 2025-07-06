# app/core/celery_app.py

from celery import Celery

from app.config.settings import settings_config


celery_app = Celery(
    settings_config.TITLE,
    broker=settings_config.RABBIT_URL,  # RabbitMQ
    backend=settings_config.REDIS_URL,  # optional to store backend into "redis://localhost:6379/0
)

celery_app.conf.task_routes = {
    "app.core.tasks.*": {"queue": "documents"},
}
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
)

# Ensure tasks are imported so they are registered
celery_app.autodiscover_tasks(['app.core'])
