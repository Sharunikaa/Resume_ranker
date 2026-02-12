"""
Pydantic models for Job.
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class ExtractedRequirements(BaseModel):
    """Requirements extracted from job description by LLM."""

    required_skills: List[str] = Field(default_factory=list)
    preferred_skills: List[str] = Field(default_factory=list)
    domain: str = ""
    experience_level: str = ""


class Weights(BaseModel):
    """Scoring weights for ranking."""

    project_weight: float = 0.4
    skill_weight: float = 0.35
    experience_weight: float = 0.25


class JobCreate(BaseModel):
    """Request body for creating a job."""

    title: str
    description: str


class JobResponse(BaseModel):
    """Job as returned by API."""

    job_id: str
    title: str
    description: str
    extracted_requirements: ExtractedRequirements = Field(default_factory=ExtractedRequirements)
    weights: Weights = Field(default_factory=Weights)
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
