# Project Architecture

## Main Flow
Frontend -> Symfony -> FastAPI -> ticket_analyser -> rag_service -> vector_db -> LLM

## Modules

### ticket_analyser
- role:
- inputs:
- outputs:
- depends on:
- logic type: business / AI / infra

### rag_service
- role:
- inputs:
- outputs:
- depends on:
- logic type: business / AI / infra

### vector_db
- role:
- inputs:
- outputs:
- depends on:
- logic type: business / AI / infra

### llm_client
- role:
- inputs:
- outputs:
- depends on:
- logic type: business / AI / infra