import os
from dotenv import load_dotenv

def load_env():
    load_dotenv()  # loads variables from .env file

def get_db_config():
    return {
        "DB_HOST": os.getenv("DB_HOST"),
        "DB_USER": os.getenv("DB_USER"),
        "DB_PASSWORD": os.getenv("DB_PASSWORD"),
        "DB_DATABASE": os.getenv("DB_DATABASE")
    }

def get_gemini_api_key():
    return os.getenv("GEMINI_API_KEY")

def get_gemini_model():
    return "gemini-2.0-flash"
