import sys
sys.path.append('..')

from backend.app.database import SessionLocal, Base, engine, User
from backend.app.main import hash_password

# Create tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Clear existing users
db.query(User).delete()

# Weak passwords
weak_passwords = ["123456", "password", "admin", "123123", "qwerty"]
for i, pwd in enumerate(weak_passwords, 1):
    hashed, salt = hash_password(pwd)
    user = User(
        username=f"user_weak_{i}",
        hashed_password=f"{salt}:{hashed}",
        password_strength="weak"
    )
    db.add(user)
    print(f"✓ Created user_weak_{i} (password: {pwd})")

# Medium passwords
medium_passwords = ["Pass123!", "Welcome2024", "Hello@World"]
for i, pwd in enumerate(medium_passwords, 1):
    hashed, salt = hash_password(pwd)
    user = User(
        username=f"user_medium_{i}",
        hashed_password=f"{salt}:{hashed}",
        password_strength="medium"
    )
    db.add(user)
    print(f"✓ Created user_medium_{i}")

db.commit()
print("\n✅ Created 8 test users")
db.close()