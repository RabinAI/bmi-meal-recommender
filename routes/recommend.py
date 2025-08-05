from fastapi import APIRouter, HTTPException, Header, Depends
from sqlalchemy.orm import Session
from langchain_community.chat_models import ChatOpenAI
import re

from database import get_db
from models.user import UserProfile,User
from utils.security import get_current_user
from config import OPENAI_API_KEY
router = APIRouter()

@router.get("/recommend-meal")
def recommend_meal(
    token: str = Header(...),
    db: Session = Depends(get_db)
):
    email = get_current_user(token)
    user = db.query(User).filter_by(email=email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    profile = db.query(UserProfile).filter_by(user_id=user.id).first()

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    llm = ChatOpenAI(temperature=0.7, openai_api_key=OPENAI_API_KEY)
    
    prompt = f"""
    Recommend a meal plan for a person with the following details:
    Age: {profile.age},
    Height: {profile.height_cm} cm,
    Weight: {profile.weight_kg} kg,
    BMI: {profile.bmi},
    Goal: {profile.goal} (cutting, bulking, maintenance)
    """
    
    response = llm.predict(prompt)

    # Parse meal plan
    structured_meal_plan = {}
    current_section = None
    meals = {}
    lines = response.splitlines()
    note_lines = []

    for line in lines:
        line = line.strip()
        if not line:
            continue
        if re.match(r"^(Breakfast|Lunch|Dinner|.*Snack):", line):
            current_section = line.replace(":", "")
            meals[current_section] = []
        elif line.startswith("-") and current_section:
            meals[current_section].append(line.lstrip("- "))
        elif not current_section:
            match_bmi = re.search(r"BMI of ([\d.]+)", line)
            if match_bmi:
                structured_meal_plan["BMI"] = float(match_bmi.group(1))
            match_goal = re.search(r"goal is (\w+)", line)
            if match_goal:
                structured_meal_plan["goal"] = match_goal.group(1)
        else:
            note_lines.append(line)

    structured_meal_plan["meals"] = meals
    if note_lines:
        structured_meal_plan["note"] = " ".join(note_lines)

    return structured_meal_plan
















