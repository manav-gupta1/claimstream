# ClaimStream 🏥⚡

> **AI-Powered Multi-Agent Clinical Clarification Desk**
> Empowering hospitals and healthcare providers to swiftly, accurately, and compliantly resolve TPA & insurance clarification queries.

---

## 📖 Overview

When healthcare providers submit claims to Third-Party Administrators (TPAs) and health insurers, claims frequently get flagged for clarification regarding medical necessity, missing documentation, or clinical discrepancies. 

**ClaimStream** is a multi-agent AI system designed to:
1. Ingest and parse TPA/insurer clarification queries.
2. Cross-reference query requirements against patient EHR/FHIR clinical records.
3. Align findings with clinical policy guidelines.
4. Synthesize comprehensive, compliant draft clarification response packages for human-in-the-loop clinical review.

---

## 🛠️ Tech Stack

### Frontend
- **Framework**: [Next.js](https://nextjs.org/) (App Router)
- **Language**: [TypeScript](https://www.typescriptlang.org/)
- **Styling**: [Tailwind CSS](https://tailwindcss.com/)
- **Linting**: ESLint

### Backend
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Runtime / Server**: Python 3.10+ / [Uvicorn](https://www.uvicorn.org/)
- **Data Validation**: Pydantic

### Future Integrations (Hackathon Roadmap)
- **Agent Orchestration**: [LangGraph](https://github.com/langchain-ai/langgraph)
- **LLM**: Gemini API
- **Data**: Synthetic FHIR/EHR JSON datasets
- **Database**: SQLite (MVP)

---

## 📁 Project Structure

```
ClaimStream/
├── frontend/                     # Next.js TypeScript + Tailwind frontend
│   ├── src/
│   │   └── app/                  # Next.js App Router (pages, layout, components)
│   ├── public/                   # Static assets
│   ├── package.json
│   ├── tsconfig.json
│   ├── .env.example
│   └── Dockerfile
├── backend/                      # FastAPI Python backend
│   ├── app/
│   │   ├── main.py               # FastAPI application & /health endpoint
│   │   ├── agents/               # Clinical clarification agents
│   │   ├── graph/                # LangGraph workflow orchestration
│   │   ├── models/               # Pydantic schemas & data models
│   │   └── data/                 # Synthetic FHIR/EHR patient data & queries
│   ├── requirements.txt          # Python dependencies
│   ├── .env.example              # Backend environment template
│   └── Dockerfile
├── docs/                         # Project & architecture documentation
│   └── ARCHITECTURE.md
├── docker-compose.yml            # Multi-service container setup
├── .gitignore                    # Git ignore configuration
└── README.md                     # Project documentation
```

---

## 🚀 Getting Started

### Prerequisites
- **Node.js**: `v18.0.0+` (or `v20+`)
- **npm**: `v9+`
- **Python**: `3.10+` (Python `3.12` recommended)
- **Docker & Docker Compose** *(Optional, for containerized run)*

---

### 1. Backend Setup

1. **Navigate to the backend directory**:
   ```bash
   cd backend
   ```

2. **Create and activate a virtual environment**:
   ```bash
   # On macOS / Linux:
   python3 -m venv .venv
   source .venv/bin/activate

   # On Windows (PowerShell):
   # python -m venv .venv
   # .venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   ```

5. **Run the FastAPI server**:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

6. **Verify Backend**:
   - **Health Check**: [http://localhost:8000/health](http://localhost:8000/health)
   - **Interactive API Docs (Swagger UI)**: [http://localhost:8000/docs](http://localhost:8000/docs)

---

### 2. Frontend Setup

1. **Navigate to the frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env.local
   ```

4. **Run the development server**:
   ```bash
   npm run dev
   ```

5. **Access the application**:
   - Open [http://localhost:3000](http://localhost:3000) in your browser.

---

### 3. Running with Docker Compose (Alternative)

To spin up both backend and frontend concurrently:

```bash
docker compose up --build
```

- **Frontend**: [http://localhost:3000](http://localhost:3000)
- **Backend API**: [http://localhost:8000](http://localhost:8000)
- **Swagger Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧪 Verification & Health Check

You can verify the backend status at any time via curl:

```bash
curl http://localhost:8000/health
```

Expected Response:
```json
{
  "status": "healthy",
  "service": "ClaimStream API"
}
```

---

## 👥 Hackathon Team Collaboration Guidelines

1. **Branching Strategy**: 
   - `main`: Stable releases.
   - `feature/<feature-name>`: Active feature branches.
2. **Environment Variables**: Never commit `.env` or `.env.local` files. Add new configuration keys to `.env.example`.
3. **Backend Modularity**:
   - Place agent logic inside `backend/app/agents/`.
   - Place LangGraph state and workflows inside `backend/app/graph/`.
   - Place Pydantic models inside `backend/app/models/`.
   - Place synthetic sample data inside `backend/app/data/`.
