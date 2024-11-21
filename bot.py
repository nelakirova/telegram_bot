import os
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext
from dotenv import load_dotenv
import logging

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Загрузка токена из .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("Токен не найден. Проверьте файл .env или переменные окружения.")

# Обработчик команды /start
async def start(update: Update, context: CallbackContext) -> None:
    keyboard = [[KeyboardButton("Go")]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "Привет! Нажми 'Go' и получи предсказание.", reply_markup=reply_markup
    )

# Обработчик команды Go
async def go(update: Update, context: CallbackContext) -> None:
    # Пример изображения (замените путь на ваш)
    await update.message.reply_photo(
        photo="https://via.placeholder.com/300", caption="Ваше предсказание!"
    )

# Основная функция
def main():
    logger.info("Запуск бота...")
    app = Application.builder().token(BOT_TOKEN).build()

    # Регистрация обработчиков
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("go", go))

    # Запуск бота
    app.run_polling()

if __name__ == "__main__":
    main()
