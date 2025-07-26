from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255))
    profile = relationship("UserProfile", back_populates="user", uselist=False)

class UserProfile(Base):
    __tablename__ = "user_profiles"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String(50))
    age = Column(Integer)
    height_cm = Column(Float)
    weight_kg = Column(Float)
    goal = Column(String(20))
    bmi = Column(Float)
    user = relationship("User", back_populates="profile")
