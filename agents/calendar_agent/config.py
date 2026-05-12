"""Central configuration for the calendar agent.

All paths are relative to the calendar_agent/ directory.
Calendar IDs are populated by scripts/create_calendars.py after OAuth.
"""
from pathlib import Path
from dotenv import load_dotenv
import os

# Load Anthropic key from existing midnight-infrastructure .env
MIDNIGHT_ENV = Path("/mnt/c/projects/midnight-infrastructure/.env")
if MIDNIGHT_ENV.exists():
    load_dotenv(MIDNIGHT_ENV)

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Paths
BASE_DIR = Path(__file__).parent
SECRETS_DIR = BASE_DIR / "secrets"
CREDENTIALS_FILE = SECRETS_DIR / "credentials.json"
TOKEN_FILE = SECRETS_DIR / "token.json"
STATE_FILE = BASE_DIR / "state.json"
DRAFT_QUEUE_DB = BASE_DIR / "draft_queue.db"
LOG_FILE = BASE_DIR / "calendar_agent.log"

# Google OAuth scopes
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/calendar.events",
]

# Calendar IDs — populated by scripts/create_calendars.py
CALENDAR_DEADLINES_ID = ""  # "TRG Deadlines"
CALENDAR_MEETINGS_ID = ""   # "TRG Meetings"

# Anthropic model — Haiku for extraction (fast, cheap, accurate enough)
EXTRACTION_MODEL = "claude-haiku-4-5"
EXTRACTION_MAX_TOKENS = 1024

# Polling
POLL_INTERVAL_MINUTES = 15
MAX_EMAILS_PER_POLL = 50

# Triage thresholds
TRIAGE_SCORE_EXTRACT = 3   # >= this score → send to LLM
TRIAGE_SCORE_FLAG = 1      # >= this score but < extract → flag for manual review
                           # below this → skip silently

# User context for the LLM (helps date resolution)
USER_TIMEZONE = "America/New_York"
USER_EMAIL = "midnight.trg@gmail.com"
