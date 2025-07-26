# from sqlalchemy import Column, Integer, String, Float, ForeignKey
# from sqlalchemy.orm import relationship
# from database import Base

# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String(50), unique=True, index=True, nullable=False)
#     email = Column(String(100), unique=True, index=True, nullable=False)
#     hashed_password = Column(String(255), nullable=False)

#     profile = relationship("UserProfile", back_populates="user", uselist=False)

# class UserProfile(Base):
#     __tablename__ = "user_profiles"
#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
#     name = Column(String(50), nullable=False)
#     age = Column(Integer, nullable=False)
#     height_cm = Column(Float, nullable=False)
#     weight_kg = Column(Float, nullable=False)
#     goal = Column(String(20), nullable=False)  # cutting, bulking, maintenance
#     bmi = Column(Float, nullable=False)

#     user = relationship("User", back_populates="profile")


from sqlalchemy.orm import Session
from schemas.user import SignupSchema,ProfileSchema
from models.user import User,UserProfile
from utils.security import get_password_hash



# --- USER ---

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, data: SignupSchema):
    hashed_pw = get_password_hash(data.password)
    user = User(
        username=data.username,
        email=data.email,
        hashed_password=hashed_pw
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_all_users(db: Session):
    return db.query(User).all()


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


# --- PROFILE ---

def get_profile_by_user_id(db: Session, user_id: int):
    return db.query(UserProfile).filter(UserProfile.user_id == user_id).first()


def create_profile(db: Session, user:User, data:ProfileSchema):
    bmi = data.weight_kg / ((data.height_cm / 100) ** 2)
    profile = UserProfile(
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
    return profile
