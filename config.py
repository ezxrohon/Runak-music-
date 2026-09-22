from os import getenv

from dotenv import load_dotenv

load_dotenv()

API_ID = int(getenv("API_ID", "0"))
API_HASH = getenv("API_HASH", "")
BOT_TOKEN = getenv("BOT_TOKEN", "")
SESSION_STRING = getenv("SESSION_STRING", "")

OWNER_ID = int(getenv("OWNER_ID", "0"))

DURATION_LIMIT = int(getenv("DURATION_LIMIT_MIN", "60")) * 60

# Firebase (Firestore) — stores which chats have used the bot, for /broadcast.
# Get a service-account key from the Firebase Console:
#   Project settings (gear icon) > Service accounts > Generate new private key
# Then provide it ONE of these two ways:
#   1) FIREBASE_CREDENTIALS_PATH — path to the downloaded JSON file, or
#   2) FIREBASE_CREDENTIALS_JSON — the whole JSON pasted as one line (handy
#      on hosts where shipping a file is awkward: Render, Railway, Heroku...)
FIREBASE_CREDENTIALS_PATH = getenv("FIREBASE_CREDENTIALS_PATH", "firebase-credentials.json")
FIREBASE_CREDENTIALS_JSON = getenv("FIREBASE_CREDENTIALS_JSON", "")

# Meow API — used to fetch the actual audio/video stream for a video id.
# Get a key from @MeowApiRobot on Telegram.
MEOW_API_URL = getenv("MEOW_API_URL", "https://music.yukiapi.site")
MEOW_API_KEY = getenv("MEOW_API_KEY", "")
