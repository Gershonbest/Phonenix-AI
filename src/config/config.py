import os
from dotenv import load_dotenv
from enum import Enum
from pathlib import Path

# Find the project root and load .env file
project_root = Path(__file__).parent.parent.parent
env_path = project_root / ".env"
load_dotenv(dotenv_path=env_path)

class Environment(Enum):
    LOCAL = "local"
    DEVELOPMENT = "development"
    PRODUCTION = "production"

    @property
    def is_local(self):
        return self in {Environment.LOCAL, Environment.DEVELOPMENT}

    @classmethod
    def from_string(cls, env_str: str):
        try:
            return cls[env_str.upper()]
        except KeyError:
            raise ValueError(f"Unknown environment: {env_str}")


class Config:
    PORT: str = os.environ.get("PORT", "8000")
    LIVEKIT_URL = os.getenv("LIVEKIT_URL")
    LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET")
    LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY")
    TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")

