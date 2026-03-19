import redis
from rq import Queue


class QueueService:

    def __init__(self):

        self.redis_conn = redis.Redis(
            host="localhost",
            port=6379,
            db=0
        )

        self.queue = Queue(
            "ticket-analysis",
            connection=self.redis_conn
        )

    def enqueue_ticket(self, ticket_text: str):

        job = self.queue.enqueue(
            "ai_service.queue.worker.process_ticket",
            ticket_text
        )

        return job.id