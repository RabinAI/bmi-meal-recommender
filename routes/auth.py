from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import timedelta

from models.user import User
from schemas.user import SignupSchema, LoginSchema
from database import get_db
from utils.security import get_password_hash, verify_password, create_access_token
from config import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()

@router.post("/signup")
def signup(data: SignupSchema, db: Session = Depends(get_db)):
    if data.password != data.retype_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    # Check if email already exists
    if db.query(User).filter_by(email=data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        username=data.username,
        email=data.email,
        hashed_password=get_password_hash(data.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User registered successfully"}

@router.post("/login")
def login(data: LoginSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=data.email).first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    }
