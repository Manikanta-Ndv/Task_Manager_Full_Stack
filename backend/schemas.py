from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    password: str = Field(..., min_length=6, max_length=50)

    @validator("username")
    def validate_username(cls, value):
        if " " in value:
            raise ValueError("Username cannot contain spaces")
        return value

class UserResponse(BaseModel):
    id: str
    username: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = None
    priority: str = Field(default="medium", pattern="^(low|medium|high)$")
    due_date: Optional[datetime] = datetime.utcnow() 
    assigned_to: Optional[str] = None
    completed: bool = False

    @validator("due_date")
    def validate_due_date(cls, value):
        if value and value < datetime.utcnow():
            raise ValueError("Due date cannot be in the past")
        return value

class TaskResponse(BaseModel):
    id: str  # Return as string, since MongoDB ObjectId is not JSON serializable
    title: str
    description: str
    priority: str
    due_date: datetime
