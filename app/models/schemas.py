from __future__ import annotations

from datetime import date
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, Field


class MatchType(StrEnum):
    STRONG = "Strong Match"
    TRANSFERABLE = "Transferable Match"
    PARTIAL = "Partial Match"
    GAP = "Gap"
    CRITICAL = "Critical Gap"


class RequirementMatch(BaseModel):
    requirement: str
    importance: Literal["high", "medium", "low"] = "medium"
    mandatory: bool = False
    match_type: MatchType
    evidence: list[str] = Field(default_factory=list)
    explanation: str
    confidence: Literal["high", "medium", "low"] = "high"


class JobAnalysis(BaseModel):
    company: str = "Unknown company"
    title: str = "Untitled role"
    location: str = "Not specified"
    employment_type: str = "Not specified"
    seniority: str = "Not specified"
    responsibilities: list[str] = Field(default_factory=list)
    required_skills: list[str] = Field(default_factory=list)
    preferred_skills: list[str] = Field(default_factory=list)
    languages: list[str] = Field(default_factory=list)
    education_requirements: list[str] = Field(default_factory=list)
    experience_requirements: list[str] = Field(default_factory=list)
    domain_requirements: list[str] = Field(default_factory=list)
    keywords: dict[str, list[str]] = Field(default_factory=dict)
    source_text: str


class ApplicationAnalysis(BaseModel):
    fit_score: int
    recommendation: str
    requirement_matches: list[RequirementMatch]
    strong_matches: list[str]
    transferable_matches: list[str]
    gaps: list[str]
    critical_gaps: list[str]
    why_you_fit: str
    main_risk: str
    score_breakdown: dict[str, int]


class CVChange(BaseModel):
    section: str
    original: str
    proposed: str
    reason: str
    evidence: list[str]
    confidence: Literal["high", "medium", "low"] = "high"


class QualityCheck(BaseModel):
    name: str
    score: int | None = None
    passed: bool
    findings: list[str] = Field(default_factory=list)


class ApplicationRecord(BaseModel):
    id: int | None = None
    company: str
    role: str
    url: str | None = None
    fit_score: int
    status: str = "Draft"
    follow_up_date: date | None = None
    notes: str = ""

