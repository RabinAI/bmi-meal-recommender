from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from database import get_db
from schemas.user import ProfileSchema
from models.user import User,UserProfile
from utils.security import get_current_user


router = APIRouter()

@router.post("/profile")
def register_profile(
    data:ProfileSchema,
    token: str = Header(...),
    db: Session = Depends(get_db)
):
    email = get_current_user(token)
    user = db.query(User).filter_by(email=email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if profile already exists
    if db.query(UserProfile).filter_by(user_id=user.id).first():
        raise HTTPException(status_code=400, detail="Profile already registered")

    bmi = data.weight_kg / ((data.height_cm / 100) ** 2)

    profile =UserProfile(
        user_id=user.id,
        name=data.name,
        age=data.age,
        height_cm=data.height_cm,
        weight_kg=data.weight_kg,
        goal=data.goal,
        bmi=round(bmi, 2)
    )

    db.add(profile)
    db.commit()
    db.refresh(profile)

    return {
        "bmi": profile.bmi,
        "message": "Profile registered successfully"
    }
