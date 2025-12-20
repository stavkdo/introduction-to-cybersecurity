"""
FastAPI Application - Complete with Database and Failed Attempts Tracking
"""
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from jose import jwt
from datetime import datetime, timedelta
import time
import os
from dotenv import load_dotenv

# Import from database.py (same folder)
from database import get_db, User, AttemptLog

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(title="Password Auth Research")

# CORS - Allow React to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration from .env
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
GROUP_SEED = int(os.getenv("GROUP_SEED", "211245440"))

# ============================================
# REQUEST/RESPONSE MODELS
# ============================================

class LoginRequest(BaseModel):
    username: str
    password: str


# ============================================
# HELPER FUNCTIONS
# ============================================

def create_token(username: str) -> str:
    """Create JWT token"""
    expire = datetime.utcnow() + timedelta(hours=24)
    return jwt.encode({"sub": username, "exp": expire}, SECRET_KEY, algorithm="HS256")


# ============================================
# API ENDPOINTS
# ============================================

@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "Password Auth Research API",
        "group_seed": GROUP_SEED,
        "docs": "/docs",
        "status": "running"
    }


@app.post("/api/login")
def login(request: LoginRequest, http_request: Request, db: Session = Depends(get_db)):
    """
    Login endpoint with failed attempts tracking
    
    Logic:
    1. Find user in database
    2. If wrong password -> increment failed_attempts
    3. If correct password -> reset failed_attempts to 0
    4. Log all attempts
    """
    start_time = time.time()
    ip = http_request.client.host if http_request.client else "unknown"
    
    print(f"login Attempt: {request.username} from {ip}")
    
    # Find user in database
    user = db.query(User).filter(User.username == request.username).first()
    
    if not user:
        # User doesn't exist
        latency = (time.time() - start_time) * 1000
        
        # Log failed attempt
        attempt = AttemptLog(
            username=request.username,
            success=False,
            latency_ms=latency,
            ip_address=ip
        )
        db.add(attempt)
        db.commit()
        
        print(f"User not found: {request.username}")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Check password
    if user.password != request.password:
        # WRONG PASSWORD
        latency = (time.time() - start_time) * 1000
        
        # INCREMENT failed_attempts
        user.failed_attempts += 1
        db.commit()
        
        print(f"Wrong password for {request.username} (failed attempts: {user.failed_attempts})")
        
        # Log failed attempt
        attempt = AttemptLog(
            username=request.username,
            success=False,
            latency_ms=latency,
            ip_address=ip
        )
        db.add(attempt)
        db.commit()
        
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # SUCCESS - Password is correct
    latency = (time.time() - start_time) * 1000
    
    # RESET failed_attempts to 0
    user.failed_attempts = 0
    db.commit()

    print(f"Login successful: {request.username} ({latency:.2f}ms) - Reset failed attempts to 0")

    # Log successful attempt
    attempt = AttemptLog(
        username=request.username,
        success=True,
        latency_ms=latency,
        ip_address=ip
    )
    db.add(attempt)
    db.commit()
    
    # Create token
    token = create_token(user.username)
    
    return {
        "success": True,
        "message": "Login successful",
        "token": token,
        "user": {
            "username": user.username,
            "password_strength": user.password_strength
        }
    }


@app.get("/api/stats")
def get_stats(db: Session = Depends(get_db)):
    """Get login statistics from database"""
    total = db.query(AttemptLog).count()
    successful = db.query(AttemptLog).filter(AttemptLog.success == True).count()
    failed = total - successful
    success_rate = round((successful / total * 100), 2) if total > 0 else 0
    
    return {
        "total_attempts": total,
        "successful": successful,
        "failed": failed,
        "success_rate": success_rate
    }


@app.get("/api/users")
def get_users(db: Session = Depends(get_db)):
    """
    Get all users with their failed attempts count
    (For debugging/testing - shows failed_attempts)
    """
    users = db.query(User).all()
    
    return {
        "total": len(users),
        "users": [
            {
                "username": user.username,
                "password_strength": user.password_strength,
                "failed_attempts": user.failed_attempts
            }
            for user in users
        ]
    }


@app.get("/health")
def health(db: Session = Depends(get_db)):
    """Health check"""
    try:
        # Test database connection
        db.execute("SELECT 1")
        user_count = db.query(User).count()
        
        return {
            "status": "healthy",
            "database": "connected",
            "users": user_count
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }