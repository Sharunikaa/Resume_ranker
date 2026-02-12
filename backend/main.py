"""
FastAPI application entrypoint.
CORS enabled; routers mounted under /api.
Loads .env from project root so MONGODB_URI, GEMINI_API_KEY, etc. are set.
"""

from pathlib import Path

from dotenv import load_dotenv

# Load .env from project root (parent of backend/)
_env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(_env_path)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes import comparison_routes, job_routes, ranking_routes, resume_routes, settings_routes

app = FastAPI(
    title="Resume Ranker API",
    description="LLM-powered multi-job resume ranking system",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check
@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(job_routes.router, prefix="/api", tags=["jobs"])
app.include_router(resume_routes.router, prefix="/api", tags=["resumes"])
app.include_router(ranking_routes.router, prefix="/api", tags=["ranking"])
app.include_router(comparison_routes.router, prefix="/api", tags=["candidates"])
app.include_router(settings_routes.router, prefix="/api", tags=["settings"])
