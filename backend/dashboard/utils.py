from fastapi import Depends, HTTPException, status
from functools import wraps

from backend.authentication.security import get_current_user
from backend.authentication.schemas import UserRole, TokenData
from backend.authentication import utils

# -----------------------------
# 🔹 Helper function
# -----------------------------
def get_user_by_id(user_id: str):
    users = utils.load_users()
    user = next((u for u in users if u["user_id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# -----------------------------
# 🔹 Role-based access decorator
# -----------------------------
def require_role(required_role: UserRole):
    """Decorator to enforce role-based access control."""
    def decorator(func):
        @wraps(func)
        def wrapper(current_user: TokenData = Depends(get_current_user), *args, **kwargs):
            if current_user.role != required_role:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Only {required_role.value}s can access this dashboard."
                )
            # Call the original route function
            return func(current_user, *args, **kwargs)
        return wrapper
    return decorator