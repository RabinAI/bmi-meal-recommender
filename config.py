import os
from dotenv import load_dotenv
load_dotenv()  # loads variables from .env into environment

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY", "dietrecomme")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:password@localhost:3306/diet")
