from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from dotenv import load_dotenv

# Load from project root
load_dotenv(os.path.join(os.path.dirname(__file__), "../../.env"))

class Settings(BaseSettings):
    app_name: str = "Buecherboerse"
    db_url: str
    secret_key: str
    testing: bool

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()

