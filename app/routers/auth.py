# This module is for user authentication, registration and login process.
# It handles:
# - User registration
# - Duplicate email and username checking
# - Password hashing and verification
# - JWT token creation and validation
# - Checking user role for admin access

from fastapi import APIRouter, HTTPException
from jose import jwt, JWTError

from app.database.database import SessionLocal
from app.models.user import User
from app.schemas.register import RegisterSchema
from app.schemas.login import loginSchema

from app.security import (
    hash_password,
    verify_password,
    make_token,
    SECRET_KEY,
    ALGORITHM
)


router = APIRouter()

@router.post("/register")
def register(data: RegisterSchema):

    db = SessionLocal()

    existing_email = db.query(User).filter(
            User.email == data.email
        ).first()

    if existing_email:
            raise HTTPException(
                status_code=409,
                detail="This email already exists!"
            )
    existing_username = db.query(User).filter(
            User.username == data.username
        ).first()

    if existing_username:
            raise HTTPException(
                status_code=409,
                detail="This username already exists!"
            )

    user_role = "USER"

    if data.admin_key == "123":
            user_role = "ADMIN"

    user = User(
            username=data.username,
            email=data.email,
            password_hash=hash_password(data.password),
            role=user_role
        )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
            "message": "User registered successfully",
            "user_id": user.id,
            "role": user.role
        }

    db.close()

@router.post("/login")
def login(data: loginSchema):

    db = SessionLocal()
    existing_user = db.query(User).filter(
            (User.email == data.email) |
            (User.username == data.username)
        ).first()

    if not existing_user:
            raise HTTPException(
                status_code=401,
                detail="Invalid username or password"
            )

    if not verify_password(
            data.password,
            existing_user.password_hash
        ):
            raise HTTPException(
                status_code=401,
                detail="Invalid username or password"
            )

    access_token = make_token(existing_user.id)

    return {
            "access_token": access_token,
            "token_type": "bearer"
        }

    db.close()
    
def get_current_user(token: str):

    db = SessionLocal()

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        user = db.query(User).filter(
            User.id == int(user_id)
        ).first()

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        return user

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    finally:
        db.close()
