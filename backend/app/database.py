"""
Database Models and Configuration
"""
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
from typing import Generator
from datetime import datetime
from app.config import DATABASE_URL

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

def get_db() -> Generator[Session, None, None]:
    """Provide database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    password_strength = Column(String(20), nullable=False)
    hash_mode = Column(String(20), nullable=False)
    totp_secret = Column(String(32), nullable=True)
    failed_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class AttemptLog(Base):
    __tablename__ = "attempt_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True, nullable=False)
    group_seed = Column(String(50), nullable=False)
    username = Column(String(100), nullable=False, index=True)
    hash_mode = Column(String(20), nullable=False)
    protection_flags = Column(String(20), nullable=False)
    result = Column(String(20), nullable=False)
    latency_ms = Column(Float, nullable=False)
    ip_address = Column(String(45))


print("[OK] Database module loaded")
print(f"[DB] {DATABASE_URL[:50] if DATABASE_URL else 'Not configured'}...")