from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(title="AI Procurement Backend", version="0.1.0")


@app.get("/")
def read_root() -> JSONResponse:
    return JSONResponse(content={"message": "AI Procurement API is running", "phase": "2"})


@app.get("/health")
def health_check() -> JSONResponse:
    return JSONResponse(content={"status": "ok"})
