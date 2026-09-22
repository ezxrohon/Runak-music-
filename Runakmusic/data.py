"""Very small Firestore wrapper — just enough to remember which chats
have used the bot, so /broadcast has somewhere to send to.

Each served chat is one document in a `served_chats` collection, keyed
by the chat id (as a string, since Firestore document ids must be strings).
"""

import json

import firebase_admin
from firebase_admin import credentials, firestore

import config

if config.FIREBASE_CREDENTIALS_JSON:
    # Raw service-account JSON in an env var — handy on hosts where you
    # can't easily ship a credentials file (Render, Railway, Heroku, ...).
    cred = credentials.Certificate(json.loads(config.FIREBASE_CREDENTIALS_JSON))
else:
    # Path to the service-account JSON file downloaded from
    # Firebase Console > Project settings > Service accounts > Generate new private key.
    cred = credentials.Certificate(config.FIREBASE_CREDENTIALS_PATH)

firebase_admin.initialize_app(cred)
db = firestore.client()
chats = db.collection("served_chats")


def add_served_chat(chat_id: int) -> None:
    chats.document(str(chat_id)).set({"chat_id": chat_id})


def remove_served_chat(chat_id: int) -> None:
    chats.document(str(chat_id)).delete()


def get_served_chats() -> list:
    return [doc.to_dict()["chat_id"] for doc in chats.stream()]
