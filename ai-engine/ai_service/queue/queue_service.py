import redis
from ai_service.infrastructure.redis_connection import get_redis_connection
from rq import Queue, Retry


class QueueService:

    def __init__(self):

        self.redis_conn = get_redis_connection() 

        self.queue = Queue(
            "ticket-analysis",
            connection=self.redis_conn
        )

    def enqueue_ticket(self, ticket_text: str):

        job = self.queue.enqueue(
            "ai_service.queue.worker.process_ticket",
            ticket_text,
            result_ttl=3600,
            retry=Retry(max=3, interval=[10, 30, 60]) # Retry up to 3 times with exponential backoff    
        )

        return job.id