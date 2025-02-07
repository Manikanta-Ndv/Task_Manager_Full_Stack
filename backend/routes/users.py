from fastapi import APIRouter, HTTPException, Depends
from database import users_collection
from schemas import UserCreate, Token
from utils import hash_password, verify_password, create_access_token
from datetime import timedelta

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register")
async def register_user(user: UserCreate):
    existing_user = await users_collection.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_password = hash_password(user.password)
    user_dict = {"username": user.username, "password": hashed_password}
    await users_collection.insert_one(user_dict)
    return {"message": "User registered successfully"}

@router.post("/login", response_model=Token)
async def login_user(user: UserCreate):
    db_user = await users_collection.find_one({"username": user.username})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
