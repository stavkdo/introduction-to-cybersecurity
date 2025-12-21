"""
Create database tables
Run ONCE after setting up PostgreSQL
"""
import sys
from pathlib import Path
from app.database import Base, engine

# Add app folder to path
sys.path.insert(0, str(Path(__file__).parent / 'app'))



print("="*60)
print("Creating database tables...")
print("="*60)

# Create all tables
Base.metadata.create_all(bind=engine)

print("Tables created successfully!")
print("   - users")
print("   - attempt_logs")
print("="*60)