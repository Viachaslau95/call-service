from celery import Celery
from src.config import config

celery = Celery(
    config.service_name,
    broker=config.celery.broker_url,
    backend=config.celery.result_backend,
    include=["src.common.celery.celery_tasks"],
)