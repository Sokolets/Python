import logging
import os
import re
import asyncio
from typing import Optional
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    CallbackContext,
    ContextTypes,
)
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Конфигурация
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
MAX_DURATION = 15 * 60  # 15 минут в секундах
TIMEOUT = 300  # 5 минут на загрузку


class Language:
    def __init__(self):
        self.strings = {
            'en': {
                'start': '🎬 <b>YouTube Video Downloader</b>\n\nSend me a YouTube link and I\'ll download the video for you!',
                'help': 'ℹ️ <b>How to use:</b>\n\n1. Send a YouTube video link\n2. Wait for download\n3. Get your video!',
                'unsupported': '❌ This is not a YouTube link. Please send a valid YouTube URL.',
                'error': '⚠️ An error occurred. Please try again later.',
                'downloading': '⏳ Downloading your video...',
                'language_set': '✅ Language has been set to English.',
                'select_language': '🌐 <b>Please select your language:</b>',
                'invalid_url': '❌ Invalid URL. Please send a valid YouTube link.',
                'too_large': '❌ Video is too large (max 50MB). Try a shorter video.',
                'not_found': '❌ Video not found or unavailable.',
                'sending': '📤 Sending your video...',
                'duration_limit': '⏱️ Video is too long (max 15 minutes).',
                'processing': '🔄 Processing your request...',
                'private': '🔒 This video is private or requires login.',
                'age_restricted': '🔞 Age-restricted content cannot be downloaded.',
                'other_bots': '🤖 <b>Check out our other bots:</b>\n\n'
                              '1. @InstagramDownloaderBot - Download Instagram videos\n'
                              '2. @TikTokSaverBot - Save TikTok videos\n'
                              '3. @UniversalMediaBot - Download from 100+ sites',
                'duration_info': '📝 <b>Note:</b> I can only download videos up to 15 minutes long.'
            },
            'ru': {
                'start': '🎬 <b>YouTube Video Downloader</b>\n\nОтправьте мне ссылку на YouTube видео, и я скачаю его для вас!',
                'help': 'ℹ️ <b>Как использовать:</b>\n\n1. Отправьте ссылку на видео YouTube\n2. Дождитесь загрузки\n3. Получите ваше видео!',
                'unsupported': '❌ Это не ссылка YouTube. Пожалуйста, отправьте действительную ссылку YouTube.',
                'error': '⚠️ Произошла ошибка. Пожалуйста, попробуйте позже.',
                'downloading': '⏳ Скачиваю ваше видео...',
                'language_set': '✅ Язык изменен на Русский.',
                'select_language': '🌐 <b>Пожалуйста, выберите ваш язык:</b>',
                'invalid_url': '❌ Неверная ссылка. Пожалуйста, отправьте действительную ссылку YouTube.',
                'too_large': '❌ Видео слишком большое (максимум 50MB).',
                'not_found': '❌ Видео не найдено или недоступно.',
                'sending': '📤 Отправляю ваше видео...',
                'duration_limit': '⏱️ Видео слишком длинное (максимум 15 минут).',
                'processing': '🔄 Обрабатываю ваш запрос...',
                'private': '🔒 Это видео приватное или требует входа.',
                'age_restricted': '🔞 Контент для взрослых не может быть загружен.',
                'other_bots': '🤖 <b>Наши другие боты:</b>\n\n'
                              '1. @InstagramDownloaderBot - Скачивание видео с Instagram\n'
                              '2. @TikTokSaverBot - Сохранение видео с TikTok\n'
                              '3. @UniversalMediaBot - Загрузка с 100+ сайтов',
                'duration_info': '📝 <b>Примечание:</b> Я могу скачивать видео длиной до 15 минут.'
            },
            'uk': {
                'start': '🎬 <b>YouTube Video Downloader</b>\n\nНадішліть мені посилання на YouTube відео, і я завантажу його для вас!',
                'help': 'ℹ️ <b>Як використовувати:</b>\n\n1. Надішліть посилання на YouTube відео\n2. Дочекайтеся завантаження\n3. Отримайте своє відео!',
                'unsupported': '❌ Це не посилання YouTube. Будь ласка, надішліть дійсне посилання YouTube.',
                'error': '⚠️ Сталася помилка. Будь ласка, спробуйте пізніше.',
                'downloading': '⏳ Завантажую ваше відео...',
                'language_set': '✅ Мову змінено на Українську.',
                'select_language': '🌐 <b>Будь ласка, оберіть вашу мову:</b>',
                'invalid_url': '❌ Неправильне посилання. Будь ласка, надішліть дійсне посилання YouTube.',
                'too_large': '❌ Відео занадто велике (максимум 50MB).',
                'not_found': '❌ Відео не знайдено або недоступне.',
                'sending': '📤 Надсилаю ваше відео...',
                'duration_limit': '⏱️ Відео занадто довге (максимум 15 хвилин).',
                'processing': '🔄 Обробляю ваш запит...',
                'private': '🔒 Це відео приватним або вимагає входу.',
                'age_restricted': '🔞 Контент для дорослих не може бути завантажений.',
                'other_bots': '🤖 <b>Наші інші боти:</b>\n\n'
                              '1. @InstagramDownloaderBot - Завантаження відео з Instagram\n'
                              '2. @TikTokSaverBot - Збереження відео з TikTok\n'
                              '3. @UniversalMediaBot - Завантаження з 100+ сайтів',
                'duration_info': '📝 <b>Примітка:</b> Я можу завантажувати відео тривалістю до 15 хвилин.'
            }
        }

    def get(self, language: str, key: str) -> str:
        return self.strings.get(language, {}).get(key, self.strings['en'][key])


lang = Language()


def get_user_language(user_data: dict) -> str:
    return user_data.get('language', 'en')


def is_youtube_url(url: str) -> bool:
    patterns = [
        r'(https?://)?(www\.)?youtube\.com/watch\?v=.+',
        r'(https?://)?(www\.)?youtube\.com/shorts/.+',
        r'(https?://)?youtu\.be/.+',
        r'(https?://)?(www\.)?youtube\.com/embed/.+',
        r'(https?://)?(www\.)?youtube\.com/v/.+'
    ]
    return any(re.match(pattern, url, re.IGNORECASE) for pattern in patterns)


async def download_youtube_video(url: str, context: CallbackContext) -> Optional[str]:
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
        'max_filesize': MAX_FILE_SIZE,
        'noplaylist': True,
        'socket_timeout': 10,
        'retries': 3,
        'fragment_retries': 3,
        'extractor_args': {
            'youtube': {
                'skip': ['dash', 'hls'],
                'player_client': ['android_embedded'],
                'player_skip': ['configs', 'webpage']
            }
        },
        'postprocessor_args': {
            'ffmpeg': ['-loglevel', 'quiet']
        },
        'merge_output_format': 'mp4',
        'http_chunk_size': 1048576,
        'consoletitle': False
    }

    try:
        os.makedirs('downloads', exist_ok=True)

        with YoutubeDL(ydl_opts) as ydl:
            info = await asyncio.to_thread(ydl.extract_info, url, download=True)

            if not info:
                return None

            if info.get('duration', 0) > MAX_DURATION:
                return 'duration_limit'

            if info.get('age_limit', 0) >= 18:
                return 'age_restricted'

            filename = ydl.prepare_filename(info)
            return filename if os.path.exists(filename) else None

    except DownloadError as e:
        if 'Private video' in str(e) or 'login' in str(e):
            return 'private'
        logger.error(f"Download error: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
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

    await update.message.reply_html(
        lang.get(language, 'start'),
        reply_markup=reply_markup
    )

    # Добавленное сообщение о 15-минутном ограничении
    await update.message.reply_html(lang.get(language, 'duration_info'))


async def help_command(update: Update, context: CallbackContext) -> None:
    user_data = context.user_data
    language = get_user_language(user_data)
    await update.message.reply_html(lang.get(language, 'help'))

    # Добавленное сообщение о 15-минутном ограничении
    await update.message.reply_html(lang.get(language, 'duration_info'))


async def language_selection(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    language_code = query.data.split('_')[1]
    context.user_data['language'] = language_code

    await query.edit_message_text(
        text=lang.get(language_code, 'language_set'),
        parse_mode='HTML'
    )

    # Добавленное сообщение о 15-минутном ограничении
    await query.message.reply_html(lang.get(language_code, 'duration_info'))


async def handle_message(update: Update, context: CallbackContext) -> None:
    user_data = context.user_data
    language = get_user_language(user_data)
    text = update.message.text.strip()

    if not re.match(r'https?://.+', text):
        await update.message.reply_html(lang.get(language, 'invalid_url'))
        return

    if not is_youtube_url(text):
        await update.message.reply_html(lang.get(language, 'unsupported'))
        return

    try:
        await update.message.reply_html(lang.get(language, 'processing'))

        video_path = await download_youtube_video(text, context)

        if video_path == 'duration_limit':
            await update.message.reply_html(lang.get(language, 'duration_limit'))
            return
        elif video_path == 'private':
            await update.message.reply_html(lang.get(language, 'private'))
            return
        elif video_path == 'age_restricted':
            await update.message.reply_html(lang.get(language, 'age_restricted'))
            return

        if video_path and os.path.exists(video_path):
            file_size = os.path.getsize(video_path)

            if file_size > MAX_FILE_SIZE:
                await update.message.reply_html(lang.get(language, 'too_large'))
            else:
                await update.message.reply_html(lang.get(language, 'sending'))
                await update.message.reply_video(
                    video=open(video_path, 'rb'),
                    supports_streaming=True,
                    read_timeout=TIMEOUT,
                    write_timeout=TIMEOUT,
                    connect_timeout=TIMEOUT,
                    pool_timeout=TIMEOUT
                )

                # Сообщение о других ботах
                await update.message.reply_html(
                    lang.get(language, 'other_bots'),
                    disable_web_page_preview=True
                )

            try:
                os.remove(video_path)
            except Exception as e:
                logger.error(f"Error deleting file: {e}")
        else:
            await update.message.reply_html(lang.get(language, 'not_found'))

    except Exception as e:
        logger.error(f"Error in handle_message: {e}")
        await update.message.reply_html(lang.get(language, 'error'))


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error("Exception while handling an update:", exc_info=context.error)

    if isinstance(update, Update) and update.message:
        user_data = context.user_data
        language = get_user_language(user_data)
        await update.message.reply_html(lang.get(language, 'error'))


def main() -> None:
    # Замените 'YOUR_BOT_TOKEN' на реальный токен
    application = Application.builder().token('7932522478:AAGP845ZDncxtJ-qhVU3T1VTpbIamEelOIw').build()

    # Регистрация обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(language_selection, pattern='^lang_'))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Обработчик ошибок
    application.add_error_handler(error_handler)

    # Запуск бота
    logger.info("Starting YouTube Downloader Bot...")
    application.run_polling(
        poll_interval=0.5,
        timeout=TIMEOUT,
        drop_pending_updates=True
    )


if __name__ == '__main__':
    # Создаем папку для загрузок
    os.makedirs('downloads', exist_ok=True)
    main()