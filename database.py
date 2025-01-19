import sqlite3


# Подключение к базе данных (создаётся файл database.db, если его нет)
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Создание таблицы пользователей
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT,
    first_name TEXT,
    last_name TEXT,
    date_joined TEXT
)
''')

# Создание таблицы для викторин
cursor.execute('''
CREATE TABLE IF NOT EXISTS quizzes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quiz_name TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    correct_answers INTEGER NOT NULL,
    total_questions INTEGER NOT NULL,
    date_taken TEXT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
''')

conn.commit()
conn.close()
