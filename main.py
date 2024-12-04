# 7725955696:AAH8CQuTRzo7r75Cur1NzSPqYSu1BeaznEg
import telebot
import sqlite3
import time
import threading

# Токен бота
API_TOKEN = '7725955696:AAH8CQuTRzo7r75Cur1NzSPqYSu1BeaznEg'
bot = telebot.TeleBot(API_TOKEN)

# Имя файла базы данных
DB_NAME = "music.db"


# Создание базы данных
def setup_database():
    """Инициализация базы данных."""
    with sqlite3.connect(DB_NAME) as db:
        cursor = db.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS songs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL
            )
        """)
        db.commit()


# Очистка базы данных каждые 1.5 месяца
def clear_database():
    while True:
        time.sleep(3600 * 24 * 45)  # 1.5 месяца
        with sqlite3.connect(DB_NAME) as db:
            cursor = db.cursor()
            cursor.execute("DELETE FROM songs")
            db.commit()
            print("База данных очищена")


# Запуск очистки базы данных в фоновом потоке
threading.Thread(target=clear_database, daemon=True).start()


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_command(message):
    # Создаем кнопки
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_add_song = telebot.types.KeyboardButton("Добавить мелодию")
    markup.add(button_add_song)

    bot.send_message(
        message.chat.id,
        f"Привет, {message.from_user.first_name}! Я бот для сохранения мелодий.",
        reply_markup=markup
    )


# Обработчик кнопки "Добавить мелодию"
@bot.message_handler(func=lambda message: message.text == "Добавить мелодию")
def add_song_handler(message):
    bot.send_message(message.chat.id, "Напишите название своей песни и также автора.")


# Обработчик текстовых сообщений для добавления песни
@bot.message_handler(func=lambda message: True)
def handle_song_input(message):
    song_title = message.text.strip()
    if song_title:
        with sqlite3.connect(DB_NAME) as db:
            cursor = db.cursor()
            cursor.execute("INSERT INTO songs (title) VALUES (?)", (song_title,))
            db.commit()
        bot.send_message(message.chat.id, "Песня успешно добавлена!")
    else:
        bot.send_message(message.chat.id, "Название песни не может быть пустым!")


# Запуск бота
if __name__ == "__main__":
    setup_database()
    print("Бот запущен!")
    bot.polling(none_stop=True)
