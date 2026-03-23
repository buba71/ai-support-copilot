# AI Support Copilot

Intelligent customer support assistance application. This project leverages the power of **RAG** (Retrieval-Augmented Generation) to analyze incoming tickets, suggest resolutions based on technical documentation, and secures decisions via a deterministic **Guardrails** engine and a **Feedback (Human-in-the-loop)** system.

---

## 🏗️ System Architecture

The project uses a decoupled architecture for performance and scalability:

```mermaid
graph TD
    Client[Browser / Vue.js 3] <--> Symfony[Backend Symfony 7.4]
    Symfony -- "HTTP POST (Port 8000)" --> FastAPI[AI Engine FastAPI]
    FastAPI <--> LLM[LLM Model GPT-4o-mini]
    FastAPI <--> ChromaDB[RAG Vector Database]
    FastAPI <--> Guardrails[Guardrail Engine]
    Symfony <--> DB[(PostgreSQL)]
    Agent[Support Agent] -- Feedback --> Symfony
```

- **Frontend**: Reactive Vue.js 3 components integrated via Symfony UX.
- **Backend (Orchestrator)**: Symfony 7.4 manages ticket lifecycles, persistence, and feedback.
- **AI Engine**: Python FastAPI service specialized in RAG and output security.

### Inter-Service Communication
The Symfony backend communicates with the AI Engine via a REST API. The endpoint is configured in `backend-symfony/config/services.yaml` under the parameter `ai_engine.endpoint` (default: `http://localhost:8000/analyze-ticket`).

### Asynchronous Queue & Worker System (AI Engine)
To prevent long-running AI tasks from blocking the main API, the project implements an asynchronous queue system using **Redis Queue (RQ)**:

1. **Redis Server**: Acts as the message broker (`localhost:6379`).
2. **QueueService**: Enqueues new AI tasks (like `ticket-analysis`) and immediately returns a `job_id` to the caller.
3. **RQ Worker**: Runs in the background (via `rq worker ticket-analysis`), continuously polling the queue to execute heavy AI tasks (RAG + LLM analysis).

```mermaid
sequenceDiagram
    actor Client as Application / API
    participant QS as QueueService
    participant Redis as Redis (Database)
    participant Worker as RQ Worker (ticket-analysis)
    participant Analyzer as TicketAnalyzer (RAG + LLM)

    Client->>QS: enqueue_ticket("Ticket content")
    QS->>Redis: Adds job to "ticket-analysis" queue
    Redis-->>QS: Returns job_id
    QS-->>Client: Returns job_id (API responds immediately)

    Note over Worker, Redis: Background Processing
    Worker->>Redis: Pops pending job from queue
    Worker->>Analyzer: Runs heavy analysis task
    Analyzer-->>Worker: Analysis result
    Worker->>Redis: Saves the result under the job_id

    Note over Client, Redis: Result Retrieval
    Client->>Redis: Fetches result using job_id
    Redis-->>Client: Returns the analysis result
```

#### 🔄 Job Lifecycle & Consumption

```mermaid
flowchart LR
    A([New Ticket]) -->|1. Enqueue| B[(Redis Queue<br/>'ticket-analysis')]
    B -->|2. Pop| C{Worker Free?}
    C -->|Yes| D[3. Execution<br/>RAG + LLM]
    D -->|4. Save Result| E[(Redis Key<br/>rq:job:id)]
    E -.->|TTL 500s expires| F([Auto-delete<br/>Free Memory])
```

1. **Enqueue**: The `QueueService` pushes the ticket into the Redis list (`rq:queue:ticket-analysis`).
2. **Dequeue (Pop)**: An available RQ Worker pops the ticket from the queue, meaning it is **consumed** and no longer waiting.
3. **Execution**: The worker runs the heavy AI analysis.
4. **Result Storage & TTL**: The return value is stored in Redis under a specific job key (e.g., `rq:job:<job_id>`). By default, RQ keeps this successful result for **500 seconds** (Time To Live) to allow the client to retrieve it. After this delay, Redis automatically deletes the result to prevent memory saturation.

#### 🧪 Testing the Queue System Locally
You can test the queue and worker sequentially using 4 separate terminal tabs, assuming a fresh start:

**Terminal 1: Start the Database (Redis & Postgres)**
Assuming your Redis server is managed by the Docker Compose file:
```bash
cd backend-symfony
docker compose up -d
```
*(If you run Redis directly on your machine, use `sudo systemctl start redis` or `redis-server`)*.

**Terminal 2: Start the AI API (FastAPI)**
```bash
cd ai-engine
# Activate your virtual environment first
source venv/bin/activate  
# Start the server
uvicorn api.main:app --reload --port 8000
```

**Terminal 3: Start the RQ Worker (Background Jobs)**
This terminal needs to be dedicated entirely to the worker so it can listen for incoming tickets in the queue.
```bash
cd ai-engine
source venv/bin/activate  
rq worker ticket-analysis
```

**Terminal 4: Run the Test Script**
Now that the API, the Database, and the Worker are all listening, trigger the test script:
```bash
cd ai-engine
source venv/bin/activate  
python test_queue.py
```

**Verification**:
- In **Terminal 4**: You will instantly see a `job_id` printed (e.g., `cf9a2...`) and the script finishes right away.
- In **Terminal 3**: You will instantly see the worker pick up the mock ticket (`"My product is broken"`) and execute the long RAG/LLM analysis process!

---

## ⚙️ Configuration (Environment Variables)

### Backend Symfony (`backend-symfony/.env`)
| Variable | Description | Default |
|----------|-------------|---------|
| `APP_ENV` | Environment (dev, prod, test) | `dev` |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://app:!ChangeMe!@127.0.0.1:5432/app` |
| `MESSENGER_TRANSPORT_DSN` | Async task transport | `doctrine://default` |

### AI Engine (`ai-engine/ai_service/.env`)
| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | Your OpenAI API key |
| `AI_MODEL_NAME` | Model name (e.g., `gpt-4o-mini`) |
| `AI_PROMPT_VERSION` | Version of the prompt being used |
| `AI_GUARDRAIL_VERSION` | Version of the guardrail rules |

---

## 🚀 Installation & Setup

### 1. Database & Docker
```bash
cd backend-symfony
docker compose up -d
# Run migrations
php bin/console doctrine:migrations:migrate
```
*Note: pgAdmin is available at [http://localhost:8080](http://localhost:8080) (admin@example.com / admin).*

### 2. Backend Symfony
```bash
cd backend-symfony
composer install
npm install
npm run build
# Start server
symfony server:start --port=8001
```

### 3. AI Service (Python)
Dependencies: `fastapi`, `uvicorn`, `pydantic`, `openai`, `chromadb`, `numpy`.
```bash
cd ai-engine
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Start API
uvicorn api.main:app --reload --port 8000
```

---

## 🎨 Frontend & Assets

The frontend is built with **Vue.js 3** integrated via **Symfony UX Vue**.
- **Location**: Components are in `backend-symfony/assets/vue/controllers/`.
- **Compilation**: Assets are managed by Webpack Encore. Use `npm run watch` during development.

---

## 🧪 Testing

### Backend (PHPUnit)
```bash
cd backend-symfony
php bin/phpunit
```

### AI Engine (Pytest)
```bash
cd ai-engine
# Activate venv first
pytest
# RAG Evaluation
python -m evaluation.evaluate_rag
```

---

## 📊 Response Example (JSON)
```json
{
  "decision": {
    "summary": "Warranty request.",
    "category": "warranty_claim",
    "urgency": "high",
    "escalation_required": true
  },
  "meta": {
    "model": "gpt-4o-mini",
    "latency_ms": 850,
    "estimated_cost": 0.00015
  }
}
```

---

## 🔧 Troubleshooting
- **Connection Refused (8000)**: Ensure the AI Engine is running (`uvicorn`).
- **Database Error**: Verify Postgres container status with `docker compose ps`.
- **Assets Not Found**: Run `npm run build` to generate the `public/build` directory.

---

## 📄 License
Proprietary
