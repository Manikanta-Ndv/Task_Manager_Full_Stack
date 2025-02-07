from fastapi import Depends, HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from database import db
from utils import SECRET_KEY, ALGORITHM
from bson import ObjectId
from database import users_collection

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# def get_current_user(token: str = Security(oauth2_scheme)):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         user_id = payload.get("sub")

#         if not user_id:
#             raise HTTPException(status_code=401, detail="Invalid token")

#         user = db.users.find_one({"_id": ObjectId(user_id)})
#         if not user:
#             raise HTTPException(status_code=401, detail="User not found")

#         return user
#     except JWTError:
#         raise HTTPException(status_code=401, detail="Invalid authentication credentials")

# def get_current_user(token: str = Depends(oauth2_scheme)):
#     if not token:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
#     return {"user": "authenticated_user"}  # Dummy example

# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     """Fetch user from DB based on token (Dummy Example)"""
#     user = await users_collection.find_one({"token": token})  # Replace with actual user lookup
#     if not user:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
#     # ✅ Return user object (including _id)
#     return user

def get_current_user(token: str = Depends(oauth2_scheme)):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No token provided")
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("sub")  # ✅ Use "sub" instead of "_id"

        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token: No user ID")

        return {"_id": user_id}  # ✅ Fix KeyError by returning "_id"

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
