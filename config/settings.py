import os
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = "https://sportapi.ai/api"
API_KEY = os.getenv("SPORTAPI_KEY")
EKSTRAKLASA_LEAGUE_ID = os.getenv("EKSTRAKLASA_LEAGUE_ID", "24")