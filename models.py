from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class ETAFeatures(BaseModel):
    party_size: int = Field(ge=1, le=20)
    waiting_parties_ahead: int = Field(ge=0)
    avg_turn_time_minutes: float = Field(gt=0)
    recent_seating_rate_per_hour: float = Field(ge=0)
    day_of_week: int = Field(ge=0, le=6)
    hour_of_day: int = Field(ge=0, le=23)


class ETAPredictionRequest(BaseModel):
    tenant_id: str
    features: ETAFeatures


class ETAPredictionResponse(BaseModel):
    tenant_id: str
    eta_minutes: int
    confidence: float
    source: str


class NoShowFeatures(BaseModel):
    party_size: int = Field(ge=1, le=20)
    elapsed_wait_minutes: float = Field(ge=0)
    quoted_wait_minutes: float = Field(ge=0)
    current_position: int = Field(ge=1)
    has_phone: bool
    opted_in_sms: bool
    historical_no_show_rate: float = Field(ge=0, le=1)


class NoShowRiskRequest(BaseModel):
    tenant_id: str
    party_id: str
    features: NoShowFeatures


class NoShowRiskResponse(BaseModel):
    tenant_id: str
    party_id: str
    risk_score: float
    risk_band: str
    recommended_action: str
    source: str


class StaffingInsightRequest(BaseModel):
    tenant_id: str
    location_name: Optional[str] = None
    historical_daily_covers: List[int] = Field(default_factory=list)
    avg_wait_minutes: float = Field(ge=0)
    no_show_rate: float = Field(ge=0, le=1)
    daypart_focus: str = "dinner"


class StaffingInsightResponse(BaseModel):
    tenant_id: str
    peak_windows: List[str]
    recommendation: str
    projected_wait_reduction_minutes: float
    source: str
    generated_at: datetime
