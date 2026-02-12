"""
Pydantic models for Candidate and structured resume.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ExperienceEntry(BaseModel):
    """Single experience entry."""

    company: str = ""
    role: str = ""
    duration: str = ""
    description: str = ""


class ProjectEntry(BaseModel):
    """Single project entry."""

    title: str = ""
    description: str = ""
    technologies: List[str] = Field(default_factory=list)
    impact: str = ""


class EducationEntry(BaseModel):
    """Single education entry."""

    degree: str = ""
    institution: str = ""
    year: str = ""


class StructuredResume(BaseModel):
    """Structured resume data extracted from PDF."""

    skills: List[str] = Field(default_factory=list)
    experience: List[ExperienceEntry] = Field(default_factory=list)
    projects: List[ProjectEntry] = Field(default_factory=list)
    education: List[EducationEntry] = Field(default_factory=list)


class Scores(BaseModel):
    """Candidate scores for a job."""

    project_similarity: float = 0.0
    skill_match: float = 0.0
    experience_match: float = 0.0
    final_score: float = 0.0


class CareerInsights(BaseModel):
    """Career trajectory insights."""

    learning_velocity: float = 0.0
    skill_evolution_rate: str = ""
    adaptability_score: float = 0.0


class CandidateCreate(BaseModel):
    """Internal: structured data when storing a candidate."""

    job_id: str
    name: str = ""
    email: str = ""
    structured_resume: StructuredResume = Field(default_factory=StructuredResume)


class CandidateResponse(BaseModel):
    """Candidate as returned by API."""

    candidate_id: str
    job_id: str
    name: str
    email: str
    structured_resume: StructuredResume = Field(default_factory=StructuredResume)
    scores: Scores = Field(default_factory=Scores)
    career_insights: CareerInsights = Field(default_factory=CareerInsights)
    rank: Optional[int] = None
    explanation: str = ""
    skill_gaps: List[str] = Field(default_factory=list)
    interview_questions: List[str] = Field(default_factory=list)
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CompareCandidatesRequest(BaseModel):
    """Request body for comparing candidates."""

    candidate_ids: List[str] = Field(..., min_length=2, max_length=5)
