"""
Create database tables
Run ONCE after setting up PostgreSQL
"""
import sys
from pathlib import Path

# Add app folder to path
sys.path.insert(0, str(Path(__file__).parent / 'app'))

from app.database import Base, engine

print("=" * 60)
print("Creating database tables...")
print("=" * 60)

# Create all tables defined in Base
Base.metadata.create_all(bind=engine)

print("[SUCCESS] Tables created successfully!")
print("   - users")
print("   - attempt_logs")
print("=" * 60)