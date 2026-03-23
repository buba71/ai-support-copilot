from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from ai_service.ticket_analyser import TicketAnalyzer
from ai_service.rag_service import RagService
from ai_service.doc_loader import load_docs
from ai_service.queue.queue_service import QueueService
from rq.job import Job
import redis

# 1. Load knowledge base at startup (optional if persistent)
# documents = load_docs("rag_docs")

rag = RagService()
queue = QueueService()

redis_conn = queue.redis_conn


app = FastAPI()
analyzer = TicketAnalyzer(rag)

class TicketRequest(BaseModel):
    ticket: str

@app.post("/analyze-ticket")
def analyze_ticket(request: TicketRequest):

    job_id = queue.enqueue_ticket(request.ticket)

    return {
        "job_id": job_id,
        "status": "queued"
    }

@app.get("/jobs/{job_id}")
def get_job(job_id: str):

    try: 
        job = Job.fetch(job_id, connection=queue.redis_conn)
    except Exception:
        raise HTTPException(status_code=404, detail="Job not found")

    if job.is_finished:
        return {
            "status": "finished",
            "result": job.result
        }

    if job.is_failed:
        return {
            "status": "failed",
        }

    return {
        "status": job.get_status()
    }

