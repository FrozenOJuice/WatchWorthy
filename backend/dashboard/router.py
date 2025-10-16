from fastapi import APIRouter, Depends, HTTPException, status
from backend.authentication.security import get_current_user
from backend.authentication.schemas import UserRole, TokenData
from backend.authentication import utils as auth_utils
from backend.dashboard import utils as dashboard_utils
from backend.reports import utils as report_utils
from backend.ratings import utils as ratings_utils

router = APIRouter(prefix="/dashboard", tags=["dashboards"])

@router.get("/member")
@dashboard_utils.require_role(UserRole.MEMBER)
def get_member_dashboard(current_user: TokenData = Depends(get_current_user)):
    user = dashboard_utils.get_user_by_id(current_user.user_id)
    penalties = report_utils.get_user_penalties(current_user.user_id)
    
    # Get user's ratings count from ratings system
    user_ratings = ratings_utils.get_user_ratings(current_user.user_id)
    
    return {
        "username": user["username"],
        "role": user["role"],
        "penalties": penalties,
        "watch_later_count": len(user.get("watch_later", [])),
        "ratings_count": len(user_ratings),  # From ratings system
        "reports_made": len(user.get("reports_made", []))
    }

@router.get("/moderator")
@dashboard_utils.require_role(UserRole.MODERATOR)
def get_moderator_dashboard(current_user: TokenData = Depends(get_current_user)):
    users = auth_utils.load_users()
    total_users = len(users)
    active_penalties = sum(len(report_utils.get_user_penalties(u["user_id"])) for u in users)
    
    # Get pending reports for moderators
    pending_reports = report_utils.get_reports_for_moderator()
    
    # Get moderation statistics
    all_reports = report_utils.load_reports()
    report_stats = {
        "pending": len([r for r in all_reports if r["status"] == "pending"]),
        "dismissed": len([r for r in all_reports if r["status"] == "dismissed"]),
        "penalty_applied": len([r for r in all_reports if r["status"] == "penalty_applied"])
    }

    return {
        "user_id": current_user.user_id,
        "role": current_user.role,
        "moderation_stats": {
            "total_users": total_users,
            "active_penalties": active_penalties,
            "total_reports": len(all_reports),
            **report_stats
        },
        "pending_reports": pending_reports[:5],
        "quick_actions": {
            "review_reports": f"/reports?status=pending",
            "view_all_reports": "/reports",
            "recent_penalties": "/reports?status=penalty_applied"
        }
    }