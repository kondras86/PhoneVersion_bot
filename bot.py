from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler
from telegram.ext.filters import UpdateType  # ✅ Важно: используем UpdateType

# Токен бота
TOKEN = '7812504089:AAGw29jvHdDqa1tPhDL3okFY1gb0y889zyw'

# URL WebApp
WEBAPP_URL = "https://your-webapp.onrender.com "

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton(
            "Определить модель телефона",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )
    ]])
    await update.message.reply_text("Нажми кнопку ниже, чтобы определить модель твоего телефона:", reply_markup=keyboard)

async def handle_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update.message.web_app_data.data
    user = update.message.from_user
    await update.message.reply_text(f"Спасибо, {user.first_name}!\nТвоя модель телефона: `{data}`", parse_mode='Markdown')
    print(f"[+] Пользователь: {user.id} | User-Agent: {data}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    
    # ✅ Используем UpdateType.WEB_APP_DATA вместо filters.WEB_APP_DATA
    app.add_handler(MessageHandler(UpdateType.WEB_APP_DATA, handle_data))

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
