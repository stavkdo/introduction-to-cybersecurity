from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
import hashlib
import secrets
from jose import jwt
from datetime import datetime, timedelta
import time
import os

from .database import engine, Base, get_db, User, AttemptLog

# Create tables
Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI(title="Password Auth Research")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET_KEY = os.getenv("SECRET_KEY", "secret")

# Schemas
class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    success: bool
    message: str
    token: str = None
    user: dict = None

# Auth utilities
def hash_password(password: str) -> tuple[str, str]:
    salt = secrets.token_hex(32)
    combined = salt + password
    password_hash = hashlib.sha256(combined.encode()).hexdigest()
    return password_hash, salt

def verify_password(password: str, salt: str, hashed: str) -> bool:
    combined = salt + password
    return hashlib.sha256(combined.encode()).hexdigest() == hashed

def create_token(username: str) -> str:
    expire = datetime.utcnow() + timedelta(hours=24)
    return jwt.encode({"sub": username, "exp": expire}, SECRET_KEY, algorithm="HS256")

# Routes
@app.get("/")
def root():
    return {"message": "Password Auth Research API"}

@app.post("/api/login", response_model=LoginResponse)
async def login(request: LoginRequest, http_request: Request, db: Session = Depends(get_db)):
    start_time = time.time()
    
    # Get user
    user = db.query(User).filter(User.username == request.username).first()
    
    if not user:
        latency = (time.time() - start_time) * 1000
        # Log attempt
        log = AttemptLog(username=request.username, success=False, latency_ms=latency)
        db.add(log)
        db.commit()
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Check if locked
    if user.locked_until and user.locked_until > datetime.utcnow():
        latency = (time.time() - start_time) * 1000
        log = AttemptLog(username=request.username, success=False, latency_ms=latency)
        db.add(log)
        db.commit()
        raise HTTPException(status_code=423, detail="Account is locked")
    
    # Verify password
    salt, hashed = user.hashed_password.split(":")
    is_valid = verify_password(request.password, salt, hashed)
    
    latency = (time.time() - start_time) * 1000
    
    if is_valid:
        # Success
        user.failed_attempts = 0
        user.locked_until = None
        token = create_token(user.username)
        
        log = AttemptLog(username=request.username, success=True, latency_ms=latency)
        db.add(log)
        db.commit()
        
        return LoginResponse(
            success=True,
            message="Login successful",
            token=token,
            user={
                "id": user.id,
                "username": user.username,
                "password_strength": user.password_strength
            }
        )
    else:
        # Failed
        user.failed_attempts += 1
        if user.failed_attempts >= 5:
            user.locked_until = datetime.utcnow() + timedelta(minutes=15)
        
        log = AttemptLog(username=request.username, success=False, latency_ms=latency)
        db.add(log)
        db.commit()
        
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/api/stats")
async def get_stats(db: Session = Depends(get_db)):
    total = db.query(AttemptLog).count()
    successful = db.query(AttemptLog).filter(AttemptLog.success == True).count()
    
    return {
        "total_attempts": total,
        "successful": successful,
        "failed": total - successful,
        "success_rate": round((successful / total * 100), 2) if total > 0 else 0
    }