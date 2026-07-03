import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    uri = os.getenv("DATABASE_URL", "postgresql://usuario:senha@localhost:5432/bookhub")
    # Correção para compatibilidade do SQLAlchemy com links do Neon/Heroku
    if uri and uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
        
    SQLALCHEMY_DATABASE_URI = uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "bookhub_secret_key_123")