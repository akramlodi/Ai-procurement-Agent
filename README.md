# AI Procurement Agent

A Next.js-based procurement intelligence MVP focused on helping a procurement officer manage procurement workspaces, upload documents, and prepare for AI-assisted supplier evaluation.

## Implemented so far

### Phase 1 — Procurement Workspace Dashboard
Completed:
- A shadcn-based procurement dashboard UI
- Create new procurement workspace flow
- Select and switch between existing workspaces
- Upload multiple procurement documents into the active workspace
- Display uploaded documents with metadata
- Local persistence of workspaces and uploaded documents in the browser

### Phase 2 — Backend Foundation for AI Processing
Completed:
- Created a backend folder with a FastAPI application
- Added a health endpoint for API validation
- Installed core AI and document-processing dependencies based on the architecture plan
- Added dependency management through backend/requirements.txt
- Prepared the backend for future LangChain, LangGraph, and document ingestion workflows

### Current stack
- Next.js 16
- React 19
- TypeScript
- Tailwind CSS
- shadcn/ui
- lucide-react
- FastAPI
- Uvicorn
- LangChain
- LangGraph
- LangSmith
- Google Generative AI client
- PyMuPDF and python-docx
- pandas and polars

## Getting started

### Frontend
1. Install frontend dependencies
   ```bash
   npm install
   ```

2. Run the frontend development server
   ```bash
   npm run dev
   ```

3. Open the app in your browser
   - Dashboard: http://localhost:3000/dashboard

### Backend
1. Navigate to the backend folder
   ```bash
   cd backend
   ```

2. Install Python dependencies
   ```bash
   python3 -m pip install -r requirements.txt
   ```

3. Run the backend API
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

4. Access the API
   - Root: http://localhost:8000/
   - Health: http://localhost:8000/health

## Project structure

- app/ - app router pages
- components/ - reusable UI components
- backend/ - FastAPI backend foundation for AI processing
- public/ - static assets

## Notes

Phase 1 covers workspace creation and document intake in the UI. Phase 2 establishes the backend foundation for future AI workflows such as document extraction, agent orchestration, retrieval, and supplier analysis.
