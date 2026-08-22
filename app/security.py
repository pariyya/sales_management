import bcrypt
from jose import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException
from app.database.database import SessionLocal
from app.models.user import User

SECRET_KEY = "abc123"
ALGORITHM = "HS256"


def hash_password(password: str):
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")


def verify_password(password: str, password_hash: str):
    return bcrypt.checkpw(
        password.encode("utf-8"),
        password_hash.encode("utf-8")
    )


def make_token(user_id: int):
    expire = datetime.utcnow() + timedelta(minutes=30)

    payload = {
        "sub": str(user_id),
        "exp": expire
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


def get_current_user(token: str):
    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )

    user_id = int(payload["sub"])

    db = SessionLocal()

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    db.close()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user

def check_admin(user):
    if user.role != "ADMIN":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    return user