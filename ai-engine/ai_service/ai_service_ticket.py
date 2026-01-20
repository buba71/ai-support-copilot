from ticket_analyser import TicketAnalyzer

if __name__ == "__main__":

    analyzer = TicketAnalyzer()

    ticket = "My order was delivered late and the box was damaged."

    result = analyzer.analyze(ticket)
    print(result)

