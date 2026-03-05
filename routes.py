from datetime import datetime
from fastapi import APIRouter, HTTPException
from models import (
    ETAPredictionRequest,
    ETAPredictionResponse,
    NoShowRiskRequest,
    NoShowRiskResponse,
    StaffingInsightRequest,
    StaffingInsightResponse,
)
from ai_service import predict_eta, score_no_show, staffing_recommendation, AIServiceError

router = APIRouter()


@router.post("/tenants/{tenant_id}/ai/eta/predict", response_model=ETAPredictionResponse)
async def ai_eta_predict(tenant_id: str, req: ETAPredictionRequest):
    if tenant_id != req.tenant_id:
        raise HTTPException(status_code=400, detail="tenant_id mismatch")

    try:
        ai_result = await predict_eta(req.model_dump())
        return ETAPredictionResponse(
            tenant_id=tenant_id,
            eta_minutes=int(ai_result["eta_minutes"]),
            confidence=float(ai_result["confidence"]),
            source=str(ai_result.get("source", "ai")),
        )
    except AIServiceError as exc:
        raise HTTPException(status_code=502, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed ETA prediction: {exc}")


@router.post("/tenants/{tenant_id}/ai/noshow/score", response_model=NoShowRiskResponse)
async def ai_noshow_score(tenant_id: str, req: NoShowRiskRequest):
    if tenant_id != req.tenant_id:
        raise HTTPException(status_code=400, detail="tenant_id mismatch")

    try:
        ai_result = await score_no_show(req.model_dump())
        return NoShowRiskResponse(
            tenant_id=tenant_id,
            party_id=req.party_id,
            risk_score=float(ai_result["risk_score"]),
            risk_band=str(ai_result["risk_band"]),
            recommended_action=str(ai_result["recommended_action"]),
            source=str(ai_result.get("source", "ai")),
        )
    except AIServiceError as exc:
        raise HTTPException(status_code=502, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed no-show scoring: {exc}")


@router.post("/tenants/{tenant_id}/ai/staffing/insights", response_model=StaffingInsightResponse)
async def ai_staffing_insights(tenant_id: str, req: StaffingInsightRequest):
    if tenant_id != req.tenant_id:
        raise HTTPException(status_code=400, detail="tenant_id mismatch")

    try:
        ai_result = await staffing_recommendation(req.model_dump())
        return StaffingInsightResponse(
            tenant_id=tenant_id,
            peak_windows=list(ai_result["peak_windows"]),
            recommendation=str(ai_result["recommendation"]),
            projected_wait_reduction_minutes=float(ai_result["projected_wait_reduction_minutes"]),
            source=str(ai_result.get("source", "ai")),
            generated_at=datetime.utcnow(),
        )
    except AIServiceError as exc:
        raise HTTPException(status_code=502, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed staffing insight generation: {exc}")
