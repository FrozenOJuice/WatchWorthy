from fastapi import APIRouter, Depends, HTTPException, status
from backend.authentication.security import get_current_user
from backend.authentication.schemas import UserRole, TokenData
from backend.authentication import utils as auth_utils
from backend.dashboard import utils as dashboard_utils

router = APIRouter(prefix="/dashboard", tags=["dashboards"])


# -----------------------------
# 🔹 Dashboards
# -----------------------------
@router.get("/member")
@dashboard_utils.require_role(UserRole.MEMBER)
def get_member_dashboard(current_user: TokenData = Depends(get_current_user)):
    user = dashboard_utils.get_user_by_id(current_user.user_id)
    return {
        "username": user["username"],
        "role": user["role"],
        "penalties": user.get("penalties", [])
    }


@router.get("/critic")
@dashboard_utils.require_role(UserRole.CRITIC)
def get_critic_dashboard(current_user: TokenData = Depends(get_current_user)):
    user = dashboard_utils.get_user_by_id(current_user.user_id)
    return {
        "username": user["username"],
        "role": user["role"],
        "reviews": user.get("reviews", []),
        "special_permissions": user.get("special_permissions", [])
    }


@router.get("/moderator")
@dashboard_utils.require_role(UserRole.MODERATOR)
def get_moderator_dashboard(current_user: TokenData = Depends(get_current_user)):
    users = auth_utils.load_users()
    total_users = len(users)
    active_penalties = sum(len(u.get("penalties", [])) for u in users)
    reported_content = sum(len(u.get("reported_content", [])) for u in users)

    return {
        "user_id": current_user.user_id,
        "role": current_user.role,
        "moderation_stats": {
            "total_users": total_users,
            "active_penalties": active_penalties,
            "reported_content": reported_content,
        }
    }


@router.get("/administrator")
@dashboard_utils.require_role(UserRole.ADMINISTRATOR)
def get_administrator_dashboard(current_user: TokenData = Depends(get_current_user)):
    users = auth_utils.load_users()
    total_users = len(users)
    active_penalties = sum(len(u.get("penalties", [])) for u in users)

    return {
        "user_id": current_user.user_id,
        "role": current_user.role,
        "system_stats": {
            "total_users": total_users,
            "active_penalties": active_penalties,
        }
    }
