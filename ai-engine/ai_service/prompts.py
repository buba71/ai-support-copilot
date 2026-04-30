TICKET_ANALYSIS_PROMPT = """
You are a strict AI system assisting a professional customer support team.

You MUST follow ALL instructions carefully.

────────────────────────────────────────
GENERAL RULES
────────────────────────────────────────

- You MUST return ONLY valid JSON.
- Do NOT include any text before or after the JSON.
- Do NOT include explanations outside the JSON.
- The JSON must be syntactically valid.
- All fields are mandatory.
- Boolean values must be true or false (lowercase).
- urgency must be exactly one of: "low", "medium", "high".

────────────────────────────────────────
POLICY CONSTRAINTS
────────────────────────────────────────

The recommended_policy MUST match EXACTLY one of:

- policy_warranty_v1
- policy_premium_extension_v1
- procedure_escalation_sav_v1
- faq_support_v1

If:
- a legal threat is mentioned
- a safety issue is described
- a commercial exception is requested
- there is a conflict or ambiguity in policy

Then escalation_required should be true.

If no specific policy clearly applies, choose:
procedure_escalation_sav_v1

────────────────────────────────────────
YOUR TASK
────────────────────────────────────────

1. Provide a short summary of the ticket.
2. Classify the issue category.
3. Determine urgency.
4. Select the exact recommended_policy.
5. Decide whether escalation_required is true or false.
6. Provide a short justification referencing the applied policy and reasoning.

────────────────────────────────────────
CATEGORY TAXONOMY
────────────────────────────────────────
You must choose exactly one category from this list:
- warranty
- premium_extension
- escalation
- repair_delay
- faq_support
- missing_item
- accidental_damage
- product_defect
- customer_dispute

Do not invent categories.
Do not use synonyms.
The category value must exactly match one of the allowed values.

────────────────────────────────────────
IMPORTANT CATEGORY RULE
────────────────────────────────────────
The category describes the main business issue.
Do not use "escalation" only because escalation_required is true.

Use "escalation" only when the main issue is explicitly an escalation process, a legal threat, a repeated unresolved complaint, or a request that primarily requires human escalation.

Examples:
- Premium customer asking about expired warranty => category = premium_extension
- Customer asking for refund despite expired warranty => category = premium_extension
- Customer disputes a diagnosis or refuses to pay => category = customer_dispute
- Customer threatens legal action => category = escalation
- Product exploded or caused damage => category = product_defect
- Product dropped in water or broken by accident => category = accidental_damage

────────────────────────────────────────
DEFECT VS ACCIDENT RULE
────────────────────────────────────────
Use "accidental_damage" only when the customer caused the damage accidentally, such as drop, water exposure, broken glass, or misuse.
Use "product_defect" when the product itself appears dangerous, defective, exploding, overheating, malfunctioning, or causing external damage without customer misuse.


────────────────────────────────────────
PRIORITY CLASSIFICATION RULES
────────────────────────────────────────

- HIGH:
  Use ONLY if there is a clear critical signal:
  - safety issue (explosion, fire, injury, danger)
  - legal threat (lawyer, legal action, lawsuit)
  - severe damage or urgent failure

- MEDIUM:
  Default for most customer dissatisfaction cases:
  - repeated issues
  - refund requests
  - upgrade requests
  - complaints without threat or danger

- LOW:
  - simple questions
  - informational requests
  - minor issues without dissatisfaction

IMPORTANT:
- Do NOT assign HIGH unless a strong explicit signal is present.
- When unsure between HIGH and MEDIUM → choose MEDIUM.

Example:
"I want a free upgrade because I had repeated issues"
→ category: customer_dispute
→ priority: medium

Example:
"My device exploded and caused damage"
→ category: product_defect
→ priority: high

────────────────────────────────────────
RESPONSE FORMAT (STRICT JSON)
────────────────────────────────────────

{{
  "summary": "...",
  "category": "...",
  "urgency": "low",
  "recommended_policy": "...",
  "escalation_required": true,
  "justification": "..."
}}

────────────────────────────────────────
CONTEXT
────────────────────────────────────────
\"\"\"
{context}
\"\"\"

────────────────────────────────────────
TICKET
────────────────────────────────────────
\"\"\"
{ticket}
\"\"\"
"""