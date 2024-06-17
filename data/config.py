import json
from dotenv import load_dotenv
import urllib.parse


load_dotenv()

#DATABASE CONGIG


IP = "129.151.207.119"
PORT = "27017"
LOGIN = "AdminMASI"
PASSWORD = "admin1488@@@@@"

DB_NAME = "MAZER_MODELS"

############
BOT_TOKEN = "6881151423:AAE5t3W3JgowNtzJQ67H_mVXlTshHvAaS1o"

with open("handlers/users/files/lang.json") as f:
    lang: dict = json.load(f)


LOGIN = urllib.parse.quote_plus(LOGIN)
PASSWORD = urllib.parse.quote_plus(PASSWORD)





