# ClaimStream

**Hackathon foundation for a clinical clarification workflow**

ClaimStream explores how a hospital team could organize responses to TPA and insurance clarification requests. The intended workflow is to parse a query, retrieve relevant clinical evidence, compare it with policy requirements, and prepare a draft for qualified human review.

> **Current status:** the checked-in application is an early project scaffold. The current backend exposes service metadata and a health endpoint. Agent, graph, model, and data packages are placeholders; the multi-agent workflow described below is planned, not implemented.

## Current implementation

- Next.js App Router frontend with a backend health-status view.
- FastAPI backend with `/` and `/health` endpoints.
- Configurable CORS origins through `CORS_ORIGINS`.
- Initial project structure for future agents, workflow orchestration, Pydantic models, and synthetic clinical data.

## Planned workflow

```text
TPA / Insurance Clarification
             |
             v
       Query Parsing
             |
             v
      Workflow Orchestrator
        /           \
       v             v
Clinical Record    Policy / Guideline
 Retrieval          Matching
       \             /
        v           v
        Evidence Aggregation
                 |
                 v
       Draft Response Synthesis
                 |
                 v
       Qualified Human Review
```

This workflow is a design target. LangGraph, an LLM provider, FHIR/EHR retrieval, and persistent storage are listed as future integrations rather than current capabilities.

## Tech stack

- **Frontend:** Next.js, React, TypeScript, Tailwind CSS.
- **Backend:** Python, FastAPI, Uvicorn.
- **Planned:** LangGraph, an LLM provider, synthetic FHIR resources, and a database.

## Repository layout

- `frontend/`: Next.js application.
- `backend/app/main.py`: FastAPI application and health endpoint.
- `backend/app/agents/`: placeholder for specialized agents.
- `backend/app/graph/`: placeholder for workflow orchestration.
- `backend/app/models/`: placeholder for schemas and data models.
- `backend/app/data/`: placeholder for synthetic clinical data.
- `docs/ARCHITECTURE.md`: intended architecture.

## Run locally

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

The health endpoint is available at `http://localhost:8000/health`.

### Frontend

```bash
cd frontend
npm install
NEXT_PUBLIC_API_URL=http://localhost:8000 npm run dev
```

Open `http://localhost:3000`. The frontend currently checks backend health; it is not yet a clinical clarification dashboard.

## Safety and scope

This project is not a clinical decision-support system and must not be used with real patient information. Any future clinical workflow must use synthetic data during development, enforce access controls and audit logging, cite source records, protect sensitive data, and require qualified human review. Generated text must never be represented as a verified clinical conclusion.

## Roadmap

- [ ] Define typed request, claim, evidence, and response schemas.
- [ ] Build a query parser with deterministic validation.
- [ ] Add synthetic FHIR/EHR fixtures and evidence retrieval.
- [ ] Implement a workflow graph with traceable state transitions.
- [ ] Add policy matching with explicit source citations.
- [ ] Add a draft response interface with mandatory human approval.
- [ ] Add persistence, authentication, audit logging, and tests.

## License

No license has been added yet. All rights reserved unless and until a license is specified.
