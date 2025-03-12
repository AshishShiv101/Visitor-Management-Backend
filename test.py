from dotenv import load_dotenv
import os

# Explicitly load the .env file
load_dotenv()

# Debug: Print environment variables
print("DATABASE_URL:", os.getenv("DATABASE_URL"))  # Should print the database URL
print("JWT_SECRET_KEY:", os.getenv("JWT_SECRET_KEY"))  # Should print the secret key

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL")
    SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default_secret_key")
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS", "False").lower() in ("true", "1", "yes")
    ALLOW_AUTO_GENERATE_TABLES = os.getenv("ALLOW_AUTO_GENERATE_TABLES", "False").lower() in ("true", "1", "yes")

    if not DATABASE_URL:
        raise ValueError("DATABASE_URL environment variable is required")
    if not SECRET_KEY:
        raise ValueError("JWT_SECRET_KEY environment variable is required")
