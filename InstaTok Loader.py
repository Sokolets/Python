import logging
import re
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    CallbackContext,
)
from yt_dlp import YoutubeDL

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class Language:
    def __init__(self):
        self.strings = {
            'en': {
                'start': 'Hello! I can download videos from TikTok and Instagram. Just send me a link!',
                'help': 'Send me a link to a video from TikTok or Instagram, and I will download it for you.',
                'unsupported': 'Sorry, this link is not supported. I can only download from TikTok and Instagram.',
                'error': 'An error occurred while processing your request. Please try again later.',
                'downloading': '📤Downloading your video...',
                'language_set': 'Language has been set to English.',
                'select_language': 'Please select your language:',
                'processing': '🔄Processing your request...',
                'invalid_url': 'This does not appear to be a valid URL. Please send a valid link.',
                'too_large': 'The video is too large to send via Telegram. Try a shorter video.',
                'not_found': '❌Video not found or unavailable.',
                'private_account': 'This is a private account. I cannot download from private accounts.',
                'login_required': 'Login required to download this content.'
            },
            'ru': {
                'start': 'Привет! Я могу скачивать видео с TikTok и Instagram. Просто отправь мне ссылку!',
                'help': 'Отправь мне ссылку на видео с TikTok или Instagram, и я скачаю его для тебя.',
                'unsupported': 'Извините, эта ссылка не поддерживается. Я могу скачивать только с TikTok и Instagram.',
                'error': 'Произошла ошибка при обработке вашего запроса. Пожалуйста, попробуйте позже.',
                'downloading': '📤Скачиваю ваше видео...',
                'language_set': 'Язык изменен на Русский.',
                'select_language': 'Пожалуйста, выберите ваш язык:',
                'processing': '🔄Обрабатываю ваш запрос...',
                'invalid_url': 'Это не похоже на корректную ссылку. Пожалуйста, отправьте действительную ссылку.',
                'too_large': 'Видео слишком большое для отправки через Telegram. Попробуйте более короткое видео.',
                'not_found': '❌Видео не найдено или недоступно.',
                'private_account': 'Это приватный аккаунт. Я не могу скачивать из приватных аккаунтов.',
                'login_required': 'Требуется вход для скачивания этого контента.'
            },
            'uk': {
                'start': 'Привіт! Я можу завантажувати відео з TikTok та Instagram. Просто надішліть мені посилання!',
                'help': 'Надішліть мені посилання на відео з TikTok або Instagram, і я завантажу його для вас.',
                'unsupported': 'Вибачте, це посилання не підтримується. Я можу завантажувати лише з TikTok та Instagram.',
                'error': 'Сталася помилка під час обробки вашого запиту. Будь ласка, спробуйте пізніше.',
                'downloading': '📤Завантажую ваше відео...',
                'language_set': 'Мову змінено на Українську.',
                'select_language': 'Будь ласка, оберіть вашу мову:',
                'processing': '🔄Обробляю ваш запит...',
                'invalid_url': 'Це не схоже на коректне посилання. Будь ласка, надішліть дійсне посилання.',
                'too_large': 'Відео занадто велике для відправки через Telegram. Спробуйте коротше відео.',
                'not_found': '❌Відео не знайдено або недоступне.',
                'private_account': 'Це закритий акаунт. Я не можу завантажувати з закритих акаунтів.',
                'login_required': 'Потрібен вхід для завантаження цього контенту.'
            }
        }

    def get(self, language, key):
        return self.strings.get(language, {}).get(key, self.strings['en'][key])


lang = Language()


def get_user_language(user_data):
    return user_data.get('language', 'en')


def is_supported_url(url):
    patterns = [
        r'(https?://)?(www\.)?tiktok\.com/.+',
        r'(https?://)?(vm\.tiktok\.com/.+)',
        r'(https?://)?(www\.instagram\.com/(p|reel|tv)/.+)',
        r'(https?://)?(instagram\.com/(p|reel|tv)/.+)'
    ]
    return any(re.match(pattern, url) for pattern in patterns)


async def download_instagram_video(url, context: CallbackContext):
    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'video.mp4',
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'force_overwrites': True,
            'noplaylist': True,
            'ignoreerrors': False,
            'geo_bypass': True,
            'geo_bypass_country': 'US',
            'cookiefile': 'cookies.txt'  # Можно добавить файл с куками для авторизации
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            if not info:
                return None

            # Проверяем, есть ли видео в результате
            if 'entries' in info:  # Это плейлист
                video = info['entries'][0]
            else:
                video = info

            if not video.get('url'):
                return None

            return 'video.mp4'

    except Exception as e:
        logger.error(f"Error downloading Instagram video: {e}")
        return None


async def download_tiktok_video(url, context: CallbackContext):
    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'video.mp4',
            'quiet': True,
            'no_warnings': True,
            'force_overwrites': True,
            'noplaylist': True
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            if not info:
                return None
            return 'video.mp4'
    except Exception as e:
        logger.error(f"Error downloading TikTok video: {e}")
        return None


async def start(update: Update, context: CallbackContext) -> None:
    user_data = context.user_data
    language = get_user_language(user_data)

    keyboard = [
        [InlineKeyboardButton("English", callback_data='lang_en')],
        [InlineKeyboardButton("Русский", callback_data='lang_ru')],
        [InlineKeyboardButton("Українська", callback_data='lang_uk')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        lang.get(language, 'select_language'),
        reply_markup=reply_markup
    )
    await update.message.reply_text(lang.get(language, 'start'))


async def help_command(update: Update, context: CallbackContext) -> None:
    user_data = context.user_data
    language = get_user_language(user_data)
    await update.message.reply_text(lang.get(language, 'help'))


async def language_selection(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    language_code = query.data.split('_')[1]
    context.user_data['language'] = language_code

    await query.edit_message_text(text=lang.get(language_code, 'language_set'))


async def handle_message(update: Update, context: CallbackContext) -> None:
    user_data = context.user_data
    language = get_user_language(user_data)
    text = update.message.text.strip()

    if not re.match(r'https?://.+', text):
        await update.message.reply_text(lang.get(language, 'invalid_url'))
        return

    if not is_supported_url(text):
        await update.message.reply_text(lang.get(language, 'unsupported'))
        return

    await update.message.reply_text(lang.get(language, 'downloading'))

    try:
        video_path = None
        if 'instagram.com' in text:
            video_path = await download_instagram_video(text, context)
        elif 'tiktok.com' in text or 'vm.tiktok.com' in text:
            video_path = await download_tiktok_video(text, context)

        if video_path and os.path.exists(video_path):
            file_size = os.path.getsize(video_path) / (1024 * 1024)
            if file_size > 50:
                await update.message.reply_text(lang.get(language, 'too_large'))
            else:
                await update.message.reply_video(video=open(video_path, 'rb'))
            os.remove(video_path)
        else:
            await update.message.reply_text(lang.get(language, 'not_found'))
    except Exception as e:
        logger.error(f"Error processing video: {e}")
        await update.message.reply_text(lang.get(language, 'error'))


async def error_handler(update: Update, context: CallbackContext) -> None:
    logger.error(msg="Exception while handling an update:", exc_info=context.error)
    user_data = context.user_data
    language = get_user_language(user_data)
    if update.message:
        await update.message.reply_text(lang.get(language, 'error'))


def main() -> None:
    application = Application.builder().token('7205976974:AAFtiH6LXD5_SP-rpN-Q1V2oCpaMNSueALU').build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(language_selection, pattern='^lang_'))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_error_handler(error_handler)

    application.run_polling()


if __name__ == '__main__':
    main()