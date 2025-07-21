from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# Токен бота (лучше вынести в переменные окружения!)
TOKEN = '7812504089:AAGw29jvHdDqa1tPhDL3okFY1gb0y889zyw'

# URL вашего WebApp (уберите лишние пробелы!)
WEBAPP_URL = "https://your-webapp.onrender.com "  # 🔴 ВАЖНО: замените на реальный URL

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
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


async def handle_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик данных из Web App"""
    if update.message and update.message.web_app_data and update.message.web_app_data.data:
        data = update.message.web_app_data.data
        user = update.message.from_user
        await update.message.reply_text(
            f"Спасибо, {user.first_name}!\nТвоя модель телефона: `{data}`",
            parse_mode='Markdown'
        )
        print(f"[+] Пользователь: {user.id} | User-Agent: {data}")
    else:
        await update.message.reply_text("Не удалось получить данные из приложения.")


def main():
    """Запуск бота"""
    app = Application.builder().token(TOKEN).build()

    # Обработчики
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, handle_data))  # ✅ Правильный фильтр

    print("✅ Бот запущен... Ожидание сообщений.")
    app.run_polling()


if __name__ == "__main__":
    main()
