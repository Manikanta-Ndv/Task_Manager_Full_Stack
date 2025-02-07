from fastapi import FastAPI, Request, HTTPException
from fastapi.security import OAuth2PasswordBearer
from routes import users, tasks
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging

app = FastAPI()
# Allow frontend to communicate with backend
origins = ["http://localhost:5174",
           "http://localhost:5173",
           "http://localhost:5175"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174"],  # Change this if the frontend is deployed
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Allow all headers
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login") 
app.include_router(users.router)
app.include_router(tasks.router) 

# Configure logging
logging.basicConfig(level=logging.INFO)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logging.info(f"➡️ {request.method} {request.url}")
    response = await call_next(request)
    logging.info(f"⬅️ Response Status: {response.status_code}")
    return response

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred"},
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@app.get("/")
async def root():
    return {"message": "Task Management API"}
