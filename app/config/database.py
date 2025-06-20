from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # App settings
    app_name: str = ""
    app_env: str = ""
    app_debug: bool = False
    
    # Database settings
    database_host: str = ""
    database_port: int = 0
    database_name: str = ""
    database_user: str = ""
    database_password: str = ""
    
    @property
    def database_url(self) -> str:
        if self.database_password:
            return f"mysql+pymysql://{self.database_user}:{self.database_password}@{self.database_host}:{self.database_port}/{self.database_name}"
        else:
            return f"mysql+pymysql://{self.database_user}@{self.database_host}:{self.database_port}/{self.database_name}"
    
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False
    }

settings = Settings()

# Database engine (seperti DB connection di Laravel)
engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class untuk models (seperti Eloquent Model)
Base = declarative_base()

# Dependency untuk get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()