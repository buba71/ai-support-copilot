from ai_service.classification.ticket_classifier import TicketClassifier

classifier = TicketClassifier()

result = classifier.classify("J'ai un problème de connexion et je ne peux pas accéder à mon compte.")

print(result.model_dump())  # Output: {'category': 'faq_support', 'urgency': 'low', 'complexity': 'low'}

