"""Configuración de la aplicación por entorno."""
import os
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-uncp-fis")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-secret-uncp-fis")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=8)
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'academico.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False
    FRONTEND_URL = os.getenv("FRONTEND_URL", "https://trabajofinaldwa.vercel.app")
    CORS_ORIGINS = os.getenv(
        "CORS_ORIGINS", "http://localhost:5173,https://trabajofinaldwa.vercel.app"
    ).split(",")
