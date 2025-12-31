# Password Authentication Research Project

--------------------------------------------

## Installation

### 1. Clone Repository
```bash
git clone <repository-url>
cd password-auth-research
```

### 2. Database Setup
```bash
psql -U postgres
CREATE DATABASE password_auth_db;
\q
```

### 3. Backend Setup
```bash
cd backend
pip install -r requirements.txt --break-system-packages
python -c "import fastapi, sqlalchemy, captcha; print('✓ All packages installed')"
```

### 4. Frontend Setup
```bash
cd ../frontend
npm install
npm list react @mui/material
```

### Backend Configuration

Edit .env db url
```python
DATABASE_URL = "postgresql://postgres:your_password@localhost/password_auth_db"
```


--------------------------------------------

## ▶️ Running the Application

### Start Backend
```bash
cd backend
uvicorn app.main:app --reload
```

Backend runs on: `http://localhost:8000`

### Start Frontend
```bash
cd frontend
npm run dev
```

Frontend runs on: `http://localhost:5173`


--------------------------------------------

## Testing

### 1. Insert Test Users
```bash
cd backend
python insert_users.py
```

Creates users: `user1`, `user2`, `user3` (password: `password123`)

### 2. Test Login Flow

1. Open `http://localhost:5173`
2. Try logging in with:
   - Username: `user1`
   - Password: `password123`
3. Test different protection modes

### 3. Test Protection Mechanisms

**LOCKOUT Mode:**
1. Try 5 wrong passwords
2. Account locks for 3 minutes
3. Verify "Account locked" message

**CAPTCHA Mode:**
1. Try 3 wrong passwords
2. CAPTCHA image appears
3. Enter code from image
4. Login with correct password

**TOTP Mode:**
1. Login triggers TOTP generation
2. Click "Show TOTP Code" button
3. Enter 6-digit code
4. Complete login

### 4. View Statistics

Navigate to Dashboard after login to see:
- Total login attempts
- Successful logins
- Failed attempts
- Success rate

---

## Scripts

### Insert Users
```bash
cd backend
python insert_users.py
```
Creates 3 test users with different password strengths.

### Delete All Users
```bash
cd backend
python delete_users.py
```
Clears all users from database (keeps table structure).

---

## 🌐 API Endpoints

### Authentication
- `POST /api/register` - Register new user
- `POST /api/login` - Login (without TOTP)
- `POST /api/login_totp` - Login with TOTP

### Configuration
- `GET /api/config` - Get protection mode and settings

### Statistics
- `GET /api/stats` - Get login attempt statistics
- `GET /api/users` - Get all users (with protection states)

### Admin/Testing
- `GET /api/get_totp?username=user1&group_seed=1215067c7` - Get TOTP code

### Health
- `GET /health` - Check system health
- `GET /` - API information

---

## 📊 Database Schema

### Users Table
```sql
- id: INTEGER (Primary Key)
- username: VARCHAR (Unique)
- password_hash: VARCHAR
- password_strength: VARCHAR (weak/medium/strong)
- hash_mode: VARCHAR (plain/sha256/bcrypt/argon2id)
- failed_attempts: INTEGER
- locked_until: TIMESTAMP
- totp_secret: VARCHAR
```

### Attempt Logs Table
```sql
- id: INTEGER (Primary Key)
- timestamp: TIMESTAMP
- group_seed: VARCHAR
- username: VARCHAR
- hash_mode: VARCHAR
- protection_flags: VARCHAR
- result: VARCHAR (SUCCESS/FAILED/LOCKED/CAPTCHA_REQUIRED/TOTP_REQUIRED)
- latency_ms: FLOAT
- ip_address: VARCHAR
```


--------------------------------------------

## 👥 Authors

- **Stav Kdoshim** (ID: 322356551)
- **Ofir Sasson** (ID: 203650296)

**Course:** Introduction to Cybersecurity (20940)  
**Institution:** The Open University of Israel  
