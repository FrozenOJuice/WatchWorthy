import os
from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta
from typing import Optional
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from backend.authentication import schemas

security_scheme = HTTPBearer()

ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Load secrets from environment
SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key")  
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({ 
        "exp": expire,
    })
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_access_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if not payload.get("sub"):
            return None  # Ensure required fields exist
        return payload
    except jwt.PyJWTError:
        return None
    
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security_scheme)):
    token = credentials.credentials
    payload = verify_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return schemas.TokenData(user_id=payload["sub"], role=payload["role"])

# Helper function to get guest token data
def get_guest_user():
    return schemas.TokenData(user_id=None, role=schemas.UserRole.GUEST)