from ai_service.queue.queue_service import QueueService

queue = QueueService()

job_id = queue.enqueue_ticket("My product is broken")

print(job_id)