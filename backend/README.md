# Backend setup

This backend folder contains the initial Python API foundation for Phase 2.

## Create or activate the virtual environment

From the project root:

```bash
cd "/Users/mohammedakram/Desktop/wbg intern/procurement_agent"
source .venv/bin/activate
```

## Install dependencies

```bash
cd backend
python -m pip install -r requirements.txt
```

## Run the API

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Notes

The current setup includes FastAPI and the core AI libraries referenced in the architecture document so the project is ready for future agent orchestration and document processing work.
