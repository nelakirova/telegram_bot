import logging
import os
import random
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ChatMemberHandler, ContextTypes

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Токен бота
BOT_TOKEN = "7734568951:AAF4ji6IHZRXn1MjO04ss9it6SFfWQgjjFo"

# Приветственное сообщение
START_MESSAGE = "Привет! Нажми на кнопку ниже, чтобы получить предсказание или узнать больше обо мне."

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(f"Пользователь {update.effective_user.first_name} нажал /start")

    # Создаём прикреплённую клавиатуру
    keyboard = [
        [KeyboardButton("Go"), KeyboardButton("О боте")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(START_MESSAGE, reply_markup=reply_markup)

# Обработчик текста кнопок
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    logger.info(f"Пользователь {update.effective_user.first_name} выбрал {user_message}")

    if user_message == "Go":
        # Папки с картинками и описаниями
        images_dir = "images/"
        descriptions_dir = "descriptions/"

        # Получение списка файлов
        images = os.listdir(images_dir) if os.path.exists(images_dir) else []
        descriptions = os.listdir(descriptions_dir) if os.path.exists(descriptions_dir) else []

        if images and descriptions:
            # Выбор случайной картинки и описания
            random_image = random.choice(images)
            description_file = os.path.splitext(random_image)[0] + ".txt"

            if description_file in descriptions:
                with open(os.path.join(descriptions_dir, description_file), "r", encoding="utf-8") as f:
                    description = f.read()
                # Отправка картинки с описанием
                await update.message.reply_photo(
                    photo=open(os.path.join(images_dir, random_image), "rb"),
                    caption=description
                )
                logger.info(f"Отправлено изображение {random_image} с описанием.")
            else:
                await update.message.reply_text("Описание для этой картинки отсутствует.")
                logger.warning(f"Описание для {random_image} не найдено.")
        else:
            await update.message.reply_text("Картинки или описания не найдены.")
            logger.error("Папка с картинками или описаниями пуста.")
    elif user_message == "О боте":
        # Обработчик кнопки "О боте"
        await update.message.reply_text(
            "Я бот, который отправляет предсказания.\n\n"
            "Нажмите кнопку 'Go', чтобы получить своё предсказание!"
        )
        logger.info("Пользователь запросил информацию о боте.")
    else:
        await update.message.reply_text("Я не понимаю эту команду. Пожалуйста, используйте кнопки.")

# Обработчик события "пользователь начал разговор с ботом"
async def new_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Когда новый пользователь начинает с ботом, отправляется приветственное сообщение
    user = update.message.from_user
    logger.info(f"Новый пользователь: {user.first_name}")
    
    # Отправляем сообщение, как будто он написал /start
    await start(update, context)

# Основная функция запуска бота
def main():
    logger.info("Запуск бота...")
    app = Application.builder().token(BOT_TOKEN).build()

    # Обработчики
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, handle_text))  # Обработка текстовых сообщений
    app.add_handler(ChatMemberHandler(new_user))  # Обработка события нового пользователя

    logger.info("Бот готов к работе.")
    app.run_polling()

# Точка входа
if __name__ == "__main__":
    main()
