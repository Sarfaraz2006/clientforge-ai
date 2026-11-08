"""Configuration settings for ClientForge AI Agent."""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file if present
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
REPORTS_DIR = BASE_DIR / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Gemini model to use for advanced reasoning
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

# Crawler settings
REQUEST_TIMEOUT = 12
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 (ClientForge-AuditBot/1.0)"
)

# Scoring thresholds & weights
WEIGHT_SEO = 0.25
WEIGHT_CONVERSION = 0.35
WEIGHT_PERFORMANCE = 0.20
WEIGHT_AI_READINESS = 0.20
