import os
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# Points to the login endpoint so Swagger UI knows how to authenticate
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Decodes the incoming JWT Bearer token and extracts the user_id.
    Ensures that every query is securely tracked to the authenticated user.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    JWT_SECRET = os.getenv("JWT_SECRET")
    if not JWT_SECRET:
        JWT_SECRET = "insecure_dev_secret_key"
        
    ALGORITHM = "HS256"
    
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        return user_id
    except jwt.PyJWTError:
        raise credentials_exception
