from ai_service.ticket_analyser import TicketAnalyzer

if __name__ == "__main__":
    analyzer = TicketAnalyzer()

    ticket = """
    My order was delivered late and the box was damaged.
    I need a replacement as soon as possible.
    """

    result = analyzer.analyze(ticket)

    print("AI RESULT:")
    print(result)
