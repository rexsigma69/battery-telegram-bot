import os
import httpx
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.request._httpxrequest import HTTPXRequest

class InsecureHTTPXRequest(HTTPXRequest):
    def _build_client(self):
        return httpx.AsyncClient(verify=False)

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEB_APP_URL = os.getenv("WEB_APP_URL")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    print(f"✅ /start from {user.username or user.first_name} (ID: {user.id})")

    keyboard = [[
        KeyboardButton("🔋 Open Battery Calculator", web_app=WebAppInfo(url=WEB_APP_URL))
    ]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "Click the button below to open the calculator:",
        reply_markup=reply_markup
    )

def main():
    request = InsecureHTTPXRequest()
    app = Application.builder().token(BOT_TOKEN).request(request).build()
    app.add_handler(CommandHandler("start", start))
    print("🚀 Bot is running.")
    app.run_polling()

if __name__ == "__main__":
    main()
