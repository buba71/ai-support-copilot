from ai_service.rag_service import RagService
from ai_service.ticket_analyser import TicketAnalyzer


def process_ticket(ticket_text: str):

    rag_service = RagService()
    analyzer = TicketAnalyzer(rag_service)
    result = analyzer.analyze(ticket_text)

    return result