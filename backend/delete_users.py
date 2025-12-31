"""
Delete all users from the user table
"""
from app.database import SessionLocal, User

def delete_all_users():
    db = SessionLocal()
    
    try:
        count = db.query(User).count()
        print(f"[INFO] Found {count} users in database")
        
        if count == 0:
            print("[INFO] Users table is already empty")
            return
        
        db.query(User).delete()
        db.commit()
        
        remaining = db.query(User).count()
        print(f"[SUCCESS] Deleted {count} users")
        
    except Exception as e:
        db.rollback()
        print(f"[ERROR] Failed to delete users: {e}")
    
    finally:
        db.close()


if __name__ == "__main__":
    print("[DELETE] Starting user deletion...")
    delete_all_users()