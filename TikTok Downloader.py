import os
import re
import requests
import telebot
from telebot import types
from urllib.parse import urlparse

TOKEN = "7880538740:AAFjAih_0pgCtbhvzheRH-M3Mixm23Gx2b8"
bot = telebot.TeleBot(TOKEN)

# Словарь с переводами
LANGUAGES = {
    'en': {
        'start': "👋 Hello! Send me a TikTok video link and I'll download it for you without watermark.",
        'help': "📌 Just send me a TikTok video link (e.g., https://vm.tiktok.com/xxxxx/) and I'll send you the video without watermark.",
        'invalid_link': "❌ Invalid TikTok link. Please send a valid link.",
        'downloading': "⏳ Downloading your video...",
        'error': "⚠️ Error downloading the video. Please try another link or try again later.",
        'language_set': "🌐 Language set to English.",
        'too_large': "📁 The video is too large to send via Telegram (max 50MB). Try a shorter video."
    },
    'ru': {
        'start': "👋 Привет! Отправь мне ссылку на видео из TikTok, и я скачаю его для тебя без водяного знака.",
        'help': "📌 Просто отправь мне ссылку на видео из TikTok (например, https://vm.tiktok.com/xxxxx/), и я пришлю тебе видео без водяного знака.",
        'invalid_link': "❌ Неверная ссылка на TikTok. Пожалуйста, отправьте действительную ссылку.",
        'downloading': "⏳ Скачиваю ваше видео...",
        'error': "⚠️ Ошибка при загрузке видео. Попробуйте другую ссылку или повторите позже.",
        'language_set': "🌐 Язык изменен на Русский.",
        'too_large': "📁 Видео слишком большое для отправки в Telegram (макс. 50MB). Попробуйте более короткое видео."
    },
    'uk': {
        'start': "👋 Привіт! Надішли мені посилання на відео з TikTok, і я завантажу його для тебе без водяного знака.",
        'help': "📌 Просто надішли мені посилання на відео з TikTok (наприклад, https://vm.tiktok.com/xxxxx/), і я надішлю тобі відео без водяного знака.",
        'invalid_link': "❌ Невірне посилання на TikTok. Будь ласка, надішліть дійсне посилання.",
        'downloading': "⏳ Завантажую ваше відео...",
        'error': "⚠️ Помилка при завантаженні відео. Спробуйте інше посилання або повторіть пізніше.",
        'language_set': "🌐 Мову змінено на Українську.",
        'too_large': "📁 Відео занадто велике для відправки в Telegram (макс. 50MB). Спробуйте коротше відео."
    }
}

user_language = {}


def send_other_projects(chat_id, language):
    """Отправляет информацию о других проектах"""
    projects_text = {
        'en': "🚀 Our other cool projects:\n\n"
              "1. @BestMemesBot - Fresh memes daily\n"
              "2. @MusicDownloaderPro - Download any song\n"
              "Try them out!",

        'ru': "🚀 Наши другие крутые проекты:\n\n"
              "1. @BestMemesBot - Свежие мемы каждый день\n"
              "2. @MusicDownloaderPro - Скачивание любой музыки\n"
              "Попробуйте их!",

        'uk': "🚀 Наші інші круті проекти:\n\n"
              "1. @BestMemesBot - Свіжі меми щодня\n"
              "2. @MusicDownloaderPro - Завантаження будь-якої музики\n"
              "Спробуйте їх!"
    }
    text = projects_text.get(language, projects_text['en'])
    bot.send_message(chat_id, text, disable_web_page_preview=True)


def is_valid_tiktok_url(url):
    """Проверяет, является ли ссылка валидным TikTok URL"""
    domains = [
        'tiktok.com',
        'vm.tiktok.com',
        'vt.tiktok.com',
        'www.tiktok.com',
        'm.tiktok.com'
    ]
    parsed = urlparse(url)
    return any(domain in parsed.netloc for domain in domains)


def download_tiktok_video(url):
    """Скачивает видео TikTok без водяного знака"""
    API_ENDPOINTS = [
        "https://api.tiklydown.eu.org/api/download",
        "https://tikdown.org/api/ajaxSearch",
        "https://www.tikwm.com/api/"
    ]

    for api_url in API_ENDPOINTS:
        try:
            if "tiklydown" in api_url:
                response = requests.get(f"{api_url}?url={url}", timeout=10)
                data = response.json()
                return data.get('video', {}).get('noWatermark')

            elif "tikdown" in api_url:
                headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
                response = requests.post(api_url, data=f"q={url}", headers=headers, timeout=10)
                data = response.json()
                return data.get('links', [{}])[0].get('a')

            elif "tikwm" in api_url:
                response = requests.get(f"{api_url}?url={url}", timeout=10)
                data = response.json()
                return data.get('data', {}).get('play')
        except:
            continue
    return None


@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Обработчик команды /start"""
    user_id = message.from_user.id
    user_language[user_id] = 'en'

    markup = types.InlineKeyboardMarkup()
    btn_en = types.InlineKeyboardButton("English", callback_data='lang_en')
    btn_ru = types.InlineKeyboardButton("Русский", callback_data='lang_ru')
    btn_uk = types.InlineKeyboardButton("Українська", callback_data='lang_uk')
    markup.add(btn_en, btn_ru, btn_uk)

    bot.reply_to(message, LANGUAGES['en']['start'], reply_markup=markup)


@bot.message_handler(commands=['help'])
def send_help(message):
    """Обработчик команды /help"""
    user_id = message.from_user.id
    lang = user_language.get(user_id, 'en')
    bot.reply_to(message, LANGUAGES[lang]['help'])


@bot.callback_query_handler(func=lambda call: call.data.startswith('lang_'))
def change_language(call):
    """Обработчик смены языка"""
    user_id = call.from_user.id
    lang = call.data.split('_')[1]
    user_language[user_id] = lang
    bot.answer_callback_query(call.id, LANGUAGES[lang]['language_set'])
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=LANGUAGES[lang]['start']
    )


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    """Обработчик текстовых сообщений"""
    user_id = message.from_user.id
    lang = user_language.get(user_id, 'en')

    if not is_valid_tiktok_url(message.text):
        bot.reply_to(message, LANGUAGES[lang]['invalid_link'])
        return

    url = message.text if message.text.startswith('http') else f'https://{message.text}'

    progress_msg = bot.reply_to(message, LANGUAGES[lang]['downloading'])

    try:
        video_url = download_tiktok_video(url)

        if not video_url:
            bot.reply_to(message, LANGUAGES[lang]['error'])
            return

        head = requests.head(video_url, allow_redirects=True, timeout=10)
        file_size = int(head.headers.get('content-length', 0))

        if file_size > 50 * 1024 * 1024:
            bot.reply_to(message, LANGUAGES[lang]['too_large'])
            return

        response = requests.get(video_url, stream=True, timeout=20)
        filename = f"tiktok_{user_id}.mp4"

        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)

        with open(filename, 'rb') as video_file:
            bot.send_video(
                message.chat.id,
                video_file,
                caption="✅ Here's your TikTok video without watermark" if lang == 'en' else
                "✅ Ваше видео из TikTok без водяного знака" if lang == 'ru' else
                "✅ Ваше відео з TikTok без водяного знака",
                timeout=100
            )

        # Отправляем информацию о других проектах
        send_other_projects(message.chat.id, lang)

        os.remove(filename)

    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, LANGUAGES[lang]['error'])
    finally:
        try:
            bot.delete_message(message.chat.id, progress_msg.message_id)
        except:
            pass


if __name__ == '__main__':
    print("Бот запущен и готов к работе!")
    bot.polling(none_stop=True)