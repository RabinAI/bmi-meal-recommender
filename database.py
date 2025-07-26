from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Replace this with your actual connection string
DATABASE_URL = "mysql+pymysql://root:Sanitya%4010@localhost:3306/diet"

# Create engine
engine = create_engine(DATABASE_URL)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
