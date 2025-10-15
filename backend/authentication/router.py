from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from backend.authentication import schemas, utils, security
import os, uuid

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post('/register', response_model=schemas.UserResponse)
async def register(user: schemas.UserCreate):
    users = utils.load_users()
    exists, message = utils.user_exists(users, user.username, user.email)
    if exists:
        raise HTTPException(status_code=400, detail=message)
    
    new_user = {
        "user_id": str(uuid.uuid4()),
        "username": user.username,
        "email": user.email,
        "hashed_password": security.hash_password(user.password),
        "role": user.role.value,
        "penalties": [],
    }

    users.append(new_user)
    utils.save_users(users)

    return {
        "user_id": new_user["user_id"],
        "username": new_user["username"],
        "email": new_user["email"],
        "role": new_user["role"],
        "penalties": new_user["penalties"],
    }

@router.post('/login', response_model=schemas.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    users = utils.load_users()
    user = next((u for u in users if u["username"] == form_data.username), None)

    if not user or not security.verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    # Create access token only
    access_token = security.create_access_token(
        data={"sub": user["user_id"], "role": user["role"]}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }

@router.post('/logout')
async def logout():
    """Simple logout endpoint - client should discard the token"""
    return {"message": "Successfully logged out"}