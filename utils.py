import json
from TelegramTextApp.database import SQL_request
import TelegramTextApp
import os
from dotenv import load_dotenv
import ast

if __name__ == "__main__":
    load_dotenv()
    TOKEN = os.getenv("BOT_TOKEN")
    DATABASE = os.getenv("DATABASE")
    DEBUG = os.getenv("DEBUG", "false").lower() in ("true", "1", "yes")
    TelegramTextApp.start(TOKEN, "bot.json", DATABASE, debug=DEBUG)

def create_users():
    # Пользователи
    SQL_request('''
    CREATE TABLE IF NOT EXISTS users (
        telegram_id INTEGER,
        moods JSON,
        topics JSON,
        friends JSON
    )''')

def moods(tta_data):
    result = SQL_request("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    if not result:
        create_users()

    telegram_id = tta_data["telegram_id"]

    moods = SQL_request("SELECT moods FROM users WHERE telegram_id=?", (telegram_id,), 'one')
    if not moods:
        moods = {"Восторг": "😁","Грусть": "😢","Равнодушие": "😐","Радость": "😊","Усталость": "😴"}
        topics = ["Партнёр", "Работа", "Учёба", "Здоровье", "Друзья"]
        moods_json = json.dumps(moods, ensure_ascii=False)
        topics_json = json.dumps(topics, ensure_ascii=False)
        SQL_request('INSERT INTO users (telegram_id, moods, topics) VALUES (?, ?, ?)', (telegram_id, moods_json, topics_json))
    else:
        moods = moods.get('moods')
    keyboard = {}
    for mood, emoji in moods.items():
        keyboard[f"mood|{mood}"] = emoji
    return keyboard

def topics(tta_data):
    telegram_id = tta_data["telegram_id"]
    topics = SQL_request("SELECT topics FROM users WHERE telegram_id=?", (telegram_id,), 'one')
    if not topics:
        return {}
    else:
        topics_data = topics.get('topics')
    topics_data = ast.literal_eval(topics_data)
    
    mood = tta_data["menu_name"].split("|")[1]
    keyboard = {}
    for topic in topics_data:
        keyboard[f"mood|{mood}|{topic}"] = topic
    return keyboard