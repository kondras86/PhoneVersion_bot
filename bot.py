from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import os
from flask import Flask
import threading

# Токен из переменной окружения
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise RuntimeError("Переменная окружения TOKEN не установлена!")

# URL вашего WebApp — обязательно используйте ваш реальный поддомен
url = os.getenv("WEB_APP_URL", DEFAULT_WEB_APP_URL).strip()
DEFAULT_WEB_APP_URL = "https://phoneversion-bot.onrender.com"

# Создаём Flask-приложение
app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Бот работает! Это служебная страница.</h1>", 200

# Функция для запуска Flask в отдельном потоке
def run_flask():
    port = int(os.getenv('PORT', 10000))
    app.run(host="0.0.0.0", port=port)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(
            "Определить модель телефона",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )]
    ])
    await update.message.reply_text(
        "Нажми кнопку ниже, чтобы определить модель твоего телефона:",
        reply_markup=keyboard
    )

# Обработчик данных из Web App
async def handle_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.web_app_data:
        data = update.message.web_app_data.data
        user = update.message.from_user
        await update.message.reply_text(
            f"Спасибо, {user.first_name}!\nТвоя модель телефона: `{data}`",
            parse_mode='Markdown'
        )
        print(f"[+] Пользователь: {user.id} | User-Agent: {data}")
    else:
        await update.message.reply_text("Не удалось получить данные.")

# Основная функция
def main():
    # Создаём приложение Telegram
    tg_app = Application.builder().token(TOKEN).build()

    # Добавляем обработчики
    tg_app.add_handler(CommandHandler("start", start))
    tg_app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, handle_data))

    # Запускаем Flask в отдельном потоке
    threading.Thread(target=run_flask, daemon=True).start()

    # Запускаем polling Telegram-бота
    print("✅ Бот запущен и слушает обновления...")
    tg_app.run_polling(drop_pending_updates=True)  # Защита от конфликтов

if __name__ == "__main__":
    main()
