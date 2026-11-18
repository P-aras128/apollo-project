
import os
from pathlib import Path
from dotenv import load_dotenv

# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env
load_dotenv(BASE_DIR / ".env")

# Apollo API configuration
APOLLO_API_KEY = os.getenv("APOLLO_API_KEY")

APOLLO_BASE_URL = "https://api.apollo.io/api/v1"

# Project directories
INPUT_DIR = BASE_DIR / "data" / "input"
OUTPUT_DIR = BASE_DIR / "data" / "output"
 