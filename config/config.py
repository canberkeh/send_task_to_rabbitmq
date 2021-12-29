import os
from pathlib import Path
from kombu import Queue
from celery.app.base import Celery
from dotenv import load_dotenv

PACKAGE_PARENT = '.'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
env_path = Path('./') / '.env'
load_dotenv(dotenv_path=env_path)

queue_name = "queue_to_feed"

config = {
    "broker_url": os.getenv("BROKER_URL"),
    "result_backend": None,
    "broker_pool_limit": 1,
    "broker_heartbeat": None,
    "broker_connection_timeout": 40,
    "task_ignore_result": True,
    "event_queue_expires": 60,
    "worker_prefetch_multiplier": 1,
    "worker_concurrency": 32,
    "worker_hijack_root_logger": False,
    "worker_max_tasks_per_child": 10,
    "reject_on_worker_lost": True,
    "buffer_while_offline": False
}

celery = Celery("tasks", broker=config["broker_url"])
celery.conf.update(**config)
celery.task_acks_late = True
celery.conf.broker_transport_options = {}

celery.conf.task_queues = (Queue(queue_name, routing_key='tasks.task_name',
                                 **{'x-queue-mode': 'lazy', 'queue_arguments': {'x-queue-mode': 'lazy'}}),
                           )