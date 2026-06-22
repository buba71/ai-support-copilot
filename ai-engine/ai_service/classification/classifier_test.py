from ai_service.classification.ticket_classifier import TicketClassifier

classifier = TicketClassifier()

result = classifier.classify("Client premium, j'ai oublié mon mot de passe")

print(result.model_dump())  # Output: {'category': 'faq_support', 'urgency': 'low', 'complexity': 'low'}

