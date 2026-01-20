TICKET_ANALYSIS_PROMPT = """
You are an AI system assisting a customer support team.

Use ONLY the following knowledge to answer:
{context}

Analyze the following ticket and return a JSON object with:
- summary: short summary
- category: issue category
- urgency: low | medium | high

Ticket:
\"\"\"
{ticket}
\"\"\"
"""