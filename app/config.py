import os

class Config:
    _db_url = os.getenv("DATABASE_URL", "sqlite:///dev.db")
    # Render / some providers return postgres:// — SQLAlchemy needs postgresql://
    SQLALCHEMY_DATABASE_URI = _db_url.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-me-in-production")