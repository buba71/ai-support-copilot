from rq import Queue
from rq.registry import FailedJobRegistry

from ai_service.dlq.dlq_service import DLQService
from ai_service.queue.redis_connection import get_redis_connection


def move_failed_jobs_to_dlq(queue_name: str = "ticket-analysis"):
    redis_conn = get_redis_connection()
    queue = Queue(queue_name, connection=redis_conn)
    registry = FailedJobRegistry(queue=queue)
    dlq = DLQService()

    for job_id in registry.get_job_ids():
        job = queue.fetch_job(job_id)

        if job is None:
            continue
        if job.meta.get("moved_to_dlq") is True:
            continue

        dlq.store(
            ticket=job.args[0] if job.args else "",
            error_type="FINAL_FAILURE",
            error_message=job.exc_info or "Unknown error",
            attempts="unknown",
            retryable=False,
            context={
                "job_id": job.id,
                "queue": queue_name,
                "status": job.get_status(),
            },
        )
        job.meta["moved_to_dlq"] = True
        job.save_meta()
        