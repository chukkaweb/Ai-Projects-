import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Database
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_USER = os.getenv("DB_USER", "app_user")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME", "analytics_db")
    
    @property
    def DATABASE_URL(self):
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # GCP & Vertex AI
    GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID", "gd-gcp-gridu-genai")
    MODEL_NAME = "gemini-2.5-flash"

    # Langfuse
    LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY", "")
    LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY", "")
    LANGFUSE_HOST = os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")