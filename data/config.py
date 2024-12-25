import json
import os

from dotenv import load_dotenv
import urllib.parse


from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build


load_dotenv()

#DATABASE CONGIG

DB_NAME = os.getenv("DB_NAME")

IP = os.getenv("IP")
PORT = os.getenv("PORT")
LOGIN = os.getenv("LOGIN")
PASSWORD = os.getenv("PASSWORD")

BOT_TOKEN = os.getenv("BOT_TOKEN")

with open("handlers/users/files/lang.json", encoding='utf-8') as f:
    lang: dict = json.load(f)


LOGIN = urllib.parse.quote_plus(LOGIN)
PASSWORD = urllib.parse.quote_plus(PASSWORD)


SCOPES = ["https://www.googleapis.com/auth/drive.file"]
SERVICE_ACCOUNT_FILE = "credentials.json"  # Path to your credentials.json file


credentials = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
drive_service = build("drive", "v3", credentials=credentials)

# Temporary folder for saving photos
TEMP_DIR = "temp_photos"
os.makedirs(TEMP_DIR, exist_ok=True)