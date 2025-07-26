from pydantic import BaseModel, EmailStr

class SignupSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    retype_password: str

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

class ProfileSchema(BaseModel):
    name: str
    age: int
    height_cm: float
    weight_kg: float
    goal: str

class Token(BaseModel):
    access_token: str
    token_type: str
