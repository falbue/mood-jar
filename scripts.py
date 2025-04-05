import sqlite3
import json

def SQL_request(request, params=(), all_data=None):  # Выполнение SQL-запросов
    connect = sqlite3.connect("database.db")
    cursor = connect.cursor()
    if request.strip().lower().startswith('select'):
        cursor.execute(request, params)
        if all_data == None: result = cursor.fetchone()
        else: result = cursor.fetchall()
        connect.close()
        return result
    else:
        cursor.execute(request, params)
        connect.commit()
        connect.close()

SQL_request("""
    CREATE TABLE IF NOT EXISTS users (
        telegram_id INTEGER,
        friends JSON,
        topics TEXT,
        jar JSON,
        moods JSON,
        notifications TEXT
    )
""")