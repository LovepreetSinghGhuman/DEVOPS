import os
from celery import Celery

RABBITMQ_USER = os.getenv("RABBITMQ_DEFAULT_USER", "guest")
RABBITMQ_PASS = os.getenv("RABBITMQ_DEFAULT_PASS", "guest")
BROKER_URL = f"pyamqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@localhost:5672//"

celery_app = Celery(
    "retail_worker",
    broker=BROKER_URL,
    backend="rpc://"
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)
