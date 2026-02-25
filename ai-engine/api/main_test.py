from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from ai_service.ticket_analyser import TicketAnalyzer
from ai_service.rag_service import RagService
from ai_service.doc_loader import load_docs

# 1. Load knowledge base at startup (optional if persistent)
# documents = load_docs("rag_docs")

rag = None


app = FastAPI()
analyzer = None

class TicketRequest(BaseModel):
    ticket: str

@app.post("/analyze-ticket")
def analyze_ticket(request: TicketRequest):
    result = analyzer.analyze(request.ticket)

    # if there is an error, raise an HTTPException
    if "error" in result:
        raise HTTPException(
            status_code=422,
            detail=result
        )
    return result