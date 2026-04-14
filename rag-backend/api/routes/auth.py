from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from database.mongoDB.conn import get_collection
import jwt
from datetime import datetime, timedelta, timezone
import uuid
import os
from models.user import SignupRequest, LoginRequest

router = APIRouter()

import bcrypt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Bcrypt strictly requires built-in python byte encoding
    return bcrypt.checkpw(
        plain_password.encode('utf-8'), 
        hashed_password.encode('utf-8') if isinstance(hashed_password, str) else hashed_password
    )

def get_password_hash(password: str) -> str:
    salt = bcrypt.gensalt()
    # Explicit 72-byte chunk limit to cleanly secure the DB without throwing the passlib proxy error
    hashed = bcrypt.hashpw(password.encode('utf-8')[:72], salt) 
    return hashed.decode('utf-8')

# JWT Setup
JWT_SECRET = os.getenv("JWT_SECRET")
if not JWT_SECRET:
    print("WARNING: JWT_SECRET not found in .env. Falling back to an insecure default for development.")
    JWT_SECRET = "insecure_dev_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)
    return encoded_jwt



@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(request: SignupRequest):
    users_collection = get_collection("users")
    
    # Check if user exists
    existing_user = await users_collection.find_one({"email": request.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
        
    # Create new user
    user_id = str(uuid.uuid4())
    hashed_password = get_password_hash(request.password)
    
    user_doc = {
        "user_id": user_id,
        "name": request.name,
        "email": request.email,
        "password": hashed_password,
        "created_at": datetime.now(timezone.utc)
    }
    
    await users_collection.insert_one(user_doc)
    
    return {
        "message": "User created successfully",
        "user_id": user_id
    }

@router.post("/login")
async def login(request: LoginRequest):
    users_collection = get_collection("users")
    
    # Find user by email
    user = await users_collection.find_one({"email": request.email})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
        
    # Verify password
    if not verify_password(request.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
        
    # Create JWT token
    access_token = create_access_token(data={"sub": user["user_id"]})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "user_id": user["user_id"],
            "name": user["name"],
            "email": user["email"]
        }
    }
