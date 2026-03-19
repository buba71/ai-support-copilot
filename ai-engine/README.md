# ai-decision-engine

## Architecture 

This project uses an asynchronous queue system to handle long-running tasks, such as AI-driven ticket analysis, without blocking the main API.

### Queue & Worker System

The system is built on **Redis Queue (RQ)**:

1. **Redis Server**: Acts as the message broker (running on `localhost:6379`).
2. **Queue (`ticket-analysis`)**: The holding area for tasks waiting to be processed.
3. **QueueService**: Enqueues new tasks (e.g., when the API receives a new ticket) and returns a `job_id`.
4. **RQ Worker**: Runs in the background (via `rq worker ticket-analysis`), listens to the queue, and executes the heavy AI tasks (RAG + LLM analysis).

### Sequence Diagram

```mermaid
sequenceDiagram
    actor Client as Application / API
    participant QS as QueueService
    participant Redis as Redis (Database)
    participant Worker as RQ Worker (ticket-analysis)
    participant Analyzer as TicketAnalyzer (RAG + LLM)

    Note over Client, Redis: 1. Asynchronous Enqueue
    Client->>QS: enqueue_ticket("My product is broken")
    QS->>Redis: Adds job to "ticket-analysis" queue
    Redis-->>QS: Returns job_id
    QS-->>Client: Returns job_id
    Note right of Client: The API returns immediately,<br/>ready for new requests!

    Note over Worker, Redis: 2. Background Processing
    Worker->>Redis: Listens to "ticket-analysis" queue
    Redis-->>Worker: Pops pending job (process_ticket)
    
    Worker->>Analyzer: Runs analyze("My product is broken")
    Note right of Analyzer: Heavy processing...<br/>(RAG search,<br/>LLM API call)
    Analyzer-->>Worker: Analysis result
    
    Worker->>Redis: Saves the result under the job_id

    Note over Client, Redis: 3. Result Retrieval (Later)
    Client->>Redis: Checks status/result for job_id
    Redis-->>Client: Returns the analysis result
```
