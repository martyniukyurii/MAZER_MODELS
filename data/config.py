import json
import os

from dotenv import load_dotenv
import urllib.parse


load_dotenv()

#DATABASE CONGIG

DB_NAME = os.getenv("DB_NAME")

IP = os.getenv("IP")
PORT = os.getenv("PORT")
LOGIN = os.getenv("LOGIN")
PASSWORD = os.getenv("PASSWORD")

BOT_TOKEN = os.getenv("BOT_TOKEN")

with open("handlers/users/files/lang.json") as f:
    lang: dict = json.load(f)


LOGIN = urllib.parse.quote_plus(LOGIN)
PASSWORD = urllib.parse.quote_plus(PASSWORD)





