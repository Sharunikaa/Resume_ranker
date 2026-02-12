"""
Job API routes: create, list, get, update.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.models.job_model import JobCreate, JobResponse
from backend.services import job_service

router = APIRouter()


class JobUpdate(BaseModel):
    description: str


@router.post("/jobs", response_model=JobResponse)
def create_job(payload: JobCreate):
    """Create a new job; LLM extracts requirements."""
    try:
        return job_service.create_job(title=payload.title, description=payload.description)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/jobs", response_model=list[JobResponse])
def list_jobs():
    """List all jobs."""
    try:
        return job_service.list_jobs()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/jobs/{job_id}", response_model=JobResponse)
def get_job(job_id: str):
    """Get job by id."""
    job = job_service.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.put("/jobs/{job_id}", response_model=JobResponse)
def update_job(job_id: str, payload: JobUpdate):
    """Update job description; re-extracts requirements."""
    try:
        job = job_service.update_job(job_id, payload.description)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        return job
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
