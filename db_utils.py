import sqlite3
from datetime import datetime


DB_PATH = "database.db"


def add_user(user_id, username, first_name, last_name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Проверяем, есть ли пользователь в базе
    cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
    if cursor.fetchone() is None:
        # Добавляем пользователя
        cursor.execute('''
        INSERT INTO users (id, username, first_name, last_name, date_joined)
        VALUES (?, ?, ?, ?, ?)
        ''', (user_id, username, first_name, last_name, datetime.now().isoformat()))
        conn.commit()

    conn.close()

def get_users():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    conn.close()
    return users

# Добавление результатов викторины
def add_quiz_result(quiz_name, user_id, correct_answers, total_questions):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO quizzes (quiz_name, user_id, correct_answers, total_questions, date_taken)
    VALUES (?, ?, ?, ?, ?)
    ''', (quiz_name, user_id, correct_answers, total_questions, datetime.now().isoformat()))
    conn.commit()
    conn.close()

# Получение результатов для всех пользователей
def get_all_quiz_results():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
    SELECT quizzes.id, quizzes.quiz_name, users.username, quizzes.correct_answers, quizzes.total_questions, quizzes.date_taken
    FROM quizzes
    JOIN users ON quizzes.user_id = users.id
    ''')
    results = cursor.fetchall()
    conn.close()
    return results

# Получение результатов по конкретному пользователю
def get_user_quiz_results(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
    SELECT quiz_name, correct_answers, total_questions, date_taken
    FROM quizzes
    WHERE user_id = ?
    ''', (user_id,))
    results = cursor.fetchall()
    conn.close()
    return results
