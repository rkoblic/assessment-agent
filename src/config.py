import os

from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
MODEL = os.environ.get("MODEL", "claude-sonnet-4-20250514")
MAX_TURNS = int(os.environ.get("MAX_TURNS", "20"))
MAX_TOKENS = 4096
DB_PATH = os.environ.get("DB_PATH", "assessments.db")


def get_client() -> Anthropic:
    return Anthropic(api_key=ANTHROPIC_API_KEY)
