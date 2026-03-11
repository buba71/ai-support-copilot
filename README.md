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
