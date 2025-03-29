import logging
import re
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = "7742400227:AAHKEm4fdluihmJwPSOwx3_-c7uu6kP0qFI"

def extract_tiktok_url(text):
    pattern = r'(https?://vm\.tiktok\.com/\S+|https?://www\.tiktok\.com/\S+)'
    match = re.search(pattern, text)
    return match.group(0) if match else None

async def download_tiktok_video(url):
    try:
        api_url = f"https://tikwm.com/api/?url={url}"
        response = requests.get(api_url)
        data = response.json()

        if data.get('code') == 0 and data.get('data'):
            video_url = data['data'].get('play')
            if video_url:
                video_response = requests.get(video_url)
                return video_response.content
        return None
    except Exception as e:
        logger.error(f"Error downloading TikTok video: {e}")
        return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Отправь мне ссылку на видео из TikTok, и я скачаю его без водяного знака."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    url = extract_tiktok_url(text)

    if url:
        await update.message.reply_text("Скачиваю видео... Пожалуйста, подождите.")
        video_data = await download_tiktok_video(url)

        if video_data:
            await update.message.reply_video(video=video_data, caption="Вот ваше видео без водяного знака!")
        else:
            await update.message.reply_text("Не удалось скачать видео. Проверьте ссылку и попробуйте снова.")
    else:
        await update.message.reply_text("Пожалуйста, отправьте корректную ссылку на видео TikTok.")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(msg="Exception while handling an update:", exc_info=context.error)
    await update.message.reply_text("Произошла ошибка. Пожалуйста, попробуйте позже.")


def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_error_handler(error_handler)
    application.run_polling()


if __name__ == '__main__':
    main()