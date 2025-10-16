from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from backend.authentication.security import get_current_user
from backend.authentication.schemas import UserRole, TokenData
from backend.reports import schemas, utils as report_utils
from backend.dashboard import utils as dashboard_utils

router = APIRouter(prefix="/reports", tags=["reports"])

@router.get("/", response_model=List[schemas.ReportResponse])
@dashboard_utils.require_role(UserRole.MODERATOR)
def get_pending_reports(
    current_user: TokenData = Depends(get_current_user),
    status: Optional[str] = Query(None, enum=["pending", "dismissed", "penalty_applied"]),
    limit: int = Query(50, ge=1, le=100)
):
    """Get reports - moderators can filter by status"""
    all_reports = report_utils.load_reports()
    
    if status:
        filtered_reports = [r for r in all_reports if r["status"] == status]
    else:
        filtered_reports = all_reports
    
    return filtered_reports[:limit]

@router.get("/{report_id}", response_model=schemas.ReportResponse)
@dashboard_utils.require_role(UserRole.MODERATOR)
def get_report_details(
    report_id: str,
    current_user: TokenData = Depends(get_current_user)
):
    """Get detailed information about a specific report"""
    report = report_utils.get_report_by_id(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    return report

@router.post("/{report_id}/dismiss")
@dashboard_utils.require_role(UserRole.MODERATOR)
def dismiss_report(
    report_id: str,
    notes: Optional[str] = None,
    current_user: TokenData = Depends(get_current_user)
):
    """Dismiss a report without taking action"""
    report = report_utils.get_report_by_id(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    if report["status"] != "pending":
        raise HTTPException(status_code=400, detail="Report already processed")
    
    success = report_utils.dismiss_report(report_id, current_user.user_id, notes)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to dismiss report")
    
    return {"message": "Report dismissed successfully", "report_id": report_id}

@router.post("/{report_id}/penalty")
@dashboard_utils.require_role(UserRole.MODERATOR)
def apply_penalty_from_report(
    report_id: str,
    penalty_data: schemas.PenaltyCreate,
    current_user: TokenData = Depends(get_current_user)
):
    """Apply a penalty based on a report"""
    report = report_utils.get_report_by_id(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    if report["status"] != "pending":
        raise HTTPException(status_code=400, detail="Report already processed")
    
    # Get the user who created the content being reported
    # For now, we'll assume the report is about a review from a specific user
    # You might need to adjust this based on your reporting logic
    from backend.authentication import utils as auth_utils
    users = auth_utils.load_users()
    
    # Find the user who should be penalized (this might need to be stored in the report)
    # For now, we'll use the penalty_data.user_id provided by moderator
    target_user = next((u for u in users if u["user_id"] == penalty_data.user_id), None)
    if not target_user:
        raise HTTPException(status_code=404, detail="User to penalize not found")
    
    # Apply the penalty
    penalty = report_utils.apply_penalty_to_user(
        user_id=penalty_data.user_id,
        reason=penalty_data.reason,
        severity=penalty_data.severity,
        duration_days=penalty_data.duration_days,
        report_id=report_id
    )
    
    # Update report status
    report_utils.update_report_status(
        report_id=report_id,
        status="penalty_applied",
        moderator_id=current_user.user_id,
        notes=f"Penalty applied: {penalty_data.severity} severity, {penalty_data.duration_days} days"
    )
    
    return {
        "message": "Penalty applied successfully",
        "report_id": report_id,
        "penalty": penalty
    }

@router.get("/user/{user_id}/penalties")
def get_user_penalties(
    user_id: str,
    current_user: TokenData = Depends(get_current_user)
):
    """Get penalties for a user (user can see their own, moderators can see any)"""
    # Users can only see their own penalties unless they're moderators
    if current_user.user_id != user_id and current_user.role not in [UserRole.MODERATOR, UserRole.ADMINISTRATOR]:
        raise HTTPException(status_code=403, detail="Not authorized to view these penalties")
    
    penalties = report_utils.get_user_penalties(user_id)
    return {"user_id": user_id, "penalties": penalties}