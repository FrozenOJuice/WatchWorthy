from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum
from datetime import datetime

class ReportStatus(str, Enum):
    PENDING = "pending"
    DISMISSED = "dismissed"
    PENALTY_APPLIED = "penalty_applied"

class ReportResolution(BaseModel):
    report_id: str
    action: ReportStatus
    penalty_severity: Optional[str] = Field(None, enum=["low", "medium", "high"])
    penalty_duration_days: Optional[int] = Field(None, ge=1, le=365)
    moderator_notes: Optional[str] = None

class ReportResponse(BaseModel):
    report_id: str
    reporter_id: str
    movie_id: str
    reason: str
    description: Optional[str]
    status: str
    created_at: str
    assigned_moderator: Optional[str]
    resolution: Optional[str]

class PenaltyCreate(BaseModel):
    user_id: str
    reason: str
    severity: str = Field(..., enum=["low", "medium", "high"])
    duration_days: int = Field(..., ge=1, le=365)
    report_id: Optional[str] = None  # Link to original report