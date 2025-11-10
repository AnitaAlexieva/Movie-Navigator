from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite база (ще се създаде автоматично в кореновата директория)
DATABASE_URL = "sqlite:///./movie_navigator.db"

# Engine – управлява връзката с базата
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Session – обект, чрез който четем/записваме в базата
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base – родителски клас за всички модели
Base = declarative_base()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()