import json
from fastapi import APIRouter, Depends, HTTPException, status
from backend.authentication.security import get_current_user
from backend.authentication.schemas import UserRole, TokenData
from backend.authentication import utils

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/member")
def get_member_dashboard(current_user: TokenData = Depends(get_current_user)):
    if current_user.role != UserRole.MEMBER:
        raise HTTPException(status_code=403, detail="Only members can access this dashboard.")

    users = utils.load_users()
    user = next((u for u in users if u["user_id"] == current_user.user_id), None)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "username": user["username"],
        "role": user["role"],
        "penalties": user.get("penalties", [])
    }

@router.get("/critic")
def get_critic_dashboard(current_user: TokenData = Depends(get_current_user)):
    if current_user.role != UserRole.CRITIC:
        raise HTTPException(status_code=403, detail="Only critics can access this dashboard.")

    users = utils.load_users()
    user = next((u for u in users if u["user_id"] == current_user.user_id), None)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "username": user["username"],
        "role": user["role"],
        "reviews": user.get("reviews", []),
        "special_permissions": user.get("special_permissions", [])
    }

@router.get("/moderator")
def get_moderator_dashboard(current_user: TokenData = Depends(get_current_user)):
    if current_user.role != UserRole.MODERATOR:
        raise HTTPException(status_code=403, detail="Only moderators can access this dashboard.")

    users = utils.load_users()
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
def get_administrator_dashboard(current_user: TokenData = Depends(get_current_user)):
    if current_user.role != UserRole.ADMINISTRATOR:
        raise HTTPException(status_code=403, detail="Only administrators can access this dashboard.")

    users = utils.load_users()
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