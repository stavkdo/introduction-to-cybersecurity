"""
Insert users from JSON
"""
import sys
import json
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent / 'app'))

from app.database import SessionLocal, User
from app.config import HASH_MODE
from app.hash_utils import hash_password

USERS_JSON_PATH = Path(__file__).parent / 'data' / 'users.json'


def load_users_from_json():
    try:
        with open(USERS_JSON_PATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"[ERROR] File not found: {USERS_JSON_PATH}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"[ERROR] Invalid JSON: {e}")
        sys.exit(1)


def insert_users():
    db = SessionLocal()
    users_data = load_users_from_json()
    
    try:
        print("=" * 60)
        print(f"Current hash mode: {HASH_MODE.value}")
        print("=" * 60)
        print("Clearing existing users...")
        db.query(User).delete()
        db.commit()
        
        print(f"Inserting {len(users_data)} users...")
        print("=" * 60)
        
        for user_data in users_data:
            password_hash = hash_password(user_data["password"], HASH_MODE)
            
            user = User(
                username=user_data["username"],
                password_hash=password_hash,
                password_strength=user_data["strength"],
                hash_mode=HASH_MODE.value,
                failed_attempts=0,
                created_at=datetime.utcnow()
            )
            db.add(user)
            
            print(f"  [OK] {user_data['username']:15} | {user_data['password']:20} | {user_data['strength']}")
        
        db.commit()
        
        print("=" * 60)
        print(f"[SUCCESS] Inserted {len(users_data)} users")
        print(f"[INFO] Hash mode: {HASH_MODE.value}")
        print(f"[INFO] Test: user1 / 123456")
        print("=" * 60)
        
    except Exception as e:
        print(f"[ERROR] {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    insert_users()