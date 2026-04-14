from pydantic import BaseModel, EmailStr

# Pydantic Schemas for Requests
class SignupRequest(BaseModel):
    name: str
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str