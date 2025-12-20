"""
Insert 30 test users into database
Run ONCE after creating tables
"""
import sys
from pathlib import Path
from datetime import datetime

# Add app folder to path
sys.path.insert(0, str(Path(__file__).parent / 'app'))

from database import SessionLocal, User

# All 30 users
users_data = [
    # Weak (10)
    {"username": "user1", "password": "123456", "strength": "weak"},
    {"username": "user2", "password": "password", "strength": "weak"},
    {"username": "user3", "password": "aaaaaa", "strength": "weak"},
    {"username": "user4", "password": "111111", "strength": "weak"},
    {"username": "user5", "password": "abc123", "strength": "weak"},
    {"username": "user6", "password": "123123", "strength": "weak"},
    {"username": "user7", "password": "letmein", "strength": "weak"},
    {"username": "user8", "password": "000000", "strength": "weak"},
    {"username": "user9", "password": "iloveyou", "strength": "weak"},
    {"username": "user10", "password": "12345", "strength": "weak"},
    
    # Medium (10)
    {"username": "user11", "password": "funky42", "strength": "medium"},
    {"username": "user12", "password": "metallica63", "strength": "medium"},
    {"username": "user13", "password": "cat77", "strength": "medium"},
    {"username": "user14", "password": "dog58", "strength": "medium"},
    {"username": "user15", "password": "louis91", "strength": "medium"},
    {"username": "user16", "password": "tommy34", "strength": "medium"},
    {"username": "user17", "password": "shakespeare26", "strength": "medium"},
    {"username": "user18", "password": "secret88", "strength": "medium"},
    {"username": "user19", "password": "music59", "strength": "medium"},
    {"username": "user20", "password": "Jazz17", "strength": "medium"},
    
    # Strong (10)
    {"username": "user21", "password": "t$Y7a!m38Pq@Lz", "strength": "strong"},
    {"username": "user22", "password": "Qp9%lA3@wF#k21", "strength": "strong"},
    {"username": "user23", "password": "mG4@Vz!8q#J2tR", "strength": "strong"},
    {"username": "user24", "password": "e@92Lp!xS#7wQv", "strength": "strong"},
    {"username": "user25", "password": "R!x7pQ4@bTm#6Y", "strength": "strong"},
    {"username": "user26", "password": "u#P3m!r9A@1xKf", "strength": "strong"},
    {"username": "user27", "password": "Zq!5hP@8tS#2Lf", "strength": "strong"},
    {"username": "user28", "password": "kF7@bS!3v#Q9pM", "strength": "strong"},
    {"username": "user29", "password": "c#R8tL!2mP@6xV", "strength": "strong"},
    {"username": "user30", "password": "J!m4xQ@7zT#9sB", "strength": "strong"},
]

def insert_users():
    db = SessionLocal()
    
    try:
        print("="*60)
        print("Clearing existing users...")
        db.query(User).delete()
        db.commit()
        
        print("Inserting 30 users...")
        print("="*60)
        
        for user_data in users_data:
            user = User(
                username=user_data["username"],
                password=user_data["password"],
                password_strength=user_data["strength"],
                created_at=datetime.utcnow()
            )
            db.add(user)
            print(f"  ✓ {user_data['username']:15} | {user_data['password']:20} | {user_data['strength']}")
        
        db.commit()
        
        print("="*60)
        print(f"Successfully inserted {len(users_data)} users")
        print("Test: user1 / 123456")
        print("="*60)
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    insert_users()