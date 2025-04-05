import config
from scripts import *
import re

def moods(tta_data):
    try: user_id = tta_data["telegram_data"].chat.id
    except: user_id = tta_data["telegram_data"].message.chat.id
    moods = SQL_request("SELECT moods FROM users WHERE telegram_id = ?", (user_id,))[0]
    moods = json.loads(moods)
    buttons = {}
    for mood, emoji in moods.items():
        buttons[f"mood:{mood}"] = emoji
    buttons["friends"] = "\\👥 Друзья"
    buttons[f"profile:{user_id}"] = "Профиль 👤"
    return buttons

def topics(tta_data):
    try: user_id = tta_data["telegram_data"].chat.id
    except: user_id = tta_data["telegram_data"].message.chat.id
    topics = SQL_request("SELECT topics FROM users WHERE telegram_id = ?", (user_id,))[0]
    topics = [topic.strip() for topic in topics.split(',')]
    buttons = {}
    for topic in topics:
        print(topics)
        data_button = f"'{''}'data"
        buttons[f"mood:{data_button}"] = topic
    return buttons


def registration(tta_data):
    try: user_id = tta_data["telegram_data"].chat.id
    except: user_id = tta_data["telegram_data"].message.chat.id
    user = SQL_request("SELECT * FROM users WHERE telegram_id = ?", (user_id,))
    if user is None:
        moods = {"Радость":"😊", "Грусть":"😢", "Равнодушие":"😐", "Восторг":"😁", "Усталость":"😴"}
        topics = ["Партнёр", "Работа", "Учёба", "Здоровье", "Друзья"]
        moods_json = json.dumps(moods, ensure_ascii=False)
        topics_json = json.dumps(topics, ensure_ascii=False)
        SQL_request("""INSERT INTO users (telegram_id, moods, topics)
                          VALUES (?, ?, ?)""", (user_id, moods_json, topics_json))

def formating_text(tta_data, text, type_text=None):
    call_data = tta_data["call_data"]
    data = tta_data['call_data']['data']

    if call_data["menu"] == "issue_iban":
        client_id = tta_data["telegram_data"].message.chat.id

    try:
        format_dict = {
        "data":data
        }

        formatted_text = text.format_map(
            {key: format_dict.get(key, None) for key in re.findall(r'\{(.*?)\}', text)}
        )
    except Exception as e:
        formatted_text = text.format_map(
            {key: format_dict.get(key, None) for key in re.findall(r'\{(.*?)\}', text)}
        )

    return formatted_text

if __name__ == "__main__":
    from TelegramTextApp import TTA
    TTA.start(
      config.API,
      "menus",
      debug=True,
      tta_experience=True,
      formating_text="formating_text"
    )