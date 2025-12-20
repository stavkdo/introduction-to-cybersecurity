
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from jose import jwt
from datetime import datetime, timedelta
import json
import time
import logging
import uvicorn
import os
from pathlib import Path

current_file_path = Path(__file__).resolve()
project_root = current_file_path.parent.parent.parent


# Setup logging (simple!)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

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

# Config (simple!)
SECRET_KEY = "your-secret-key"
GROUP_SEED = 211245440 ^ 322356551

# Storage
attempts = []

# Schemas
class LoginRequest(BaseModel):
    username: str
    password: str

# Helpers
def load_users():
    """Load users from JSON file"""
    users_file_path = project_root/'data'/'users.json'

    try:
        with open(users_file_path, 'r') as file:
            users = json.load(file)
        logger.info(f"Loaded {len(users)} users")
        return users
    except FileNotFoundError:
        logger.error("users.json not found!")
        logger.error(f"Files actually in this folder: {os.listdir(project_root)}")
        raise HTTPException(status_code=503, detail="Service unavailable")

def create_token(username: str):
    """Create JWT token"""
    expire = datetime.utcnow() + timedelta(hours=24)
    return jwt.encode({"sub": username, "exp": expire}, SECRET_KEY, algorithm="HS256")

def get_password_strength(password: str):
    """Check password strength"""
    if len(password) <= 6 or password.isdigit():
        return "weak"
    elif len(password) > 12:
        return "strong"
    return "medium"

# Routes
@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "Password Auth Research API",
        "group_seed": GROUP_SEED,
        "docs": "/docs"
    }

@app.post("/api/login")
async def login(request: LoginRequest, http_request: Request):
    """Login endpoint"""
    start = time.time()
    ip = 'http://127.0.0.1:5000' #http_request.client.host
    
    logger.info(f"Login attempt: {request.username} from {ip}")
    
    # Load users
    users = load_users()
    
    # Find user
    user = next((u for u in users if u["username"] == request.username), None)
    
    if not user:
        # Log failed attempt
        latency = (time.time() - start) * 1000
        attempts.append({
            "username": request.username,
            "success": False,
            "latency_ms": latency,
            "timestamp": datetime.utcnow().isoformat()
        })
        logger.warning(f"User not found: {request.username}")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Check password
    if user["password"] != request.password:
        latency = (time.time() - start) * 1000
        attempts.append({
            "username": request.username,
            "success": False,
            "latency_ms": latency,
            "timestamp": datetime.utcnow().isoformat()
        })
        logger.warning(f"Invalid password for: {request.username}")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Success!
    latency = (time.time() - start) * 1000
    attempts.append({
        "username": request.username,
        "success": True,
        "latency_ms": latency,
        "timestamp": datetime.utcnow().isoformat()
    })
    
    logger.info(f"Login successful: {request.username} ({latency:.2f}ms)")
    
    return {
        "success": True,
        "message": "Login successful",
        "token": create_token(user["username"]),
        "user": {
            "username": user["username"],
            "password_strength": get_password_strength(user["password"])
        }
    }

@app.get("/api/stats")
def get_stats():
    """Get login statistics"""
    total = len(attempts)
    successful = sum(1 for a in attempts if a["success"])
    
    return {
        "total_attempts": total,
        "successful": successful,
        "failed": total - successful,
        "success_rate": round((successful / total * 100), 2) if total > 0 else 0
    }

@app.get("/health")
def health():
    """Health check"""
    return {
        "status": "healthy",
        "total_attempts": len(attempts)
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)