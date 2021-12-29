from config.config import celery, queue_name

celery.send_task("tasks.task_name", queue=queue_name,
                 kwargs = {"message" : "message",
                           "task" : "tasks"})


