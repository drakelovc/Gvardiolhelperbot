import random
import hashlib
from datetime import datetime
from zoneinfo import ZoneInfo
from telegram import Update, InlineQueryResultPhoto
from telegram.ext import ApplicationBuilder, CommandHandler, InlineQueryHandler, ContextTypes
import uuid

BOT_TOKEN = "8790414747:AAG5qfKOBs6J_oHIBBNTVnzNYkY9ioCxVn0"
PHOTO_URL = "https://i.ibb.co/VPg7bSd/Screenshot-2026-04-02-23-34-02-351-org-telegram-messenger-edit.jpg"
KYIV_TZ = ZoneInfo("Europe/Kyiv")

NAMES_WEIGHTS = [
    ("Freshl", 0.5),
    ("Anton", 0.7),
    ("Yurets", 1.0),
    ("Drake", 2.0),
    ("Dranniy", 2.0),
    ("Nurs", 2.5),
    ("Zenox", 2.5),
    ("Bagrat", 2.5),
    ("Vadim", 2.5),
    ("Nurali", 2.5),
    ("Musa", 2.0),
    ("Dronchik", 2.0),
    ("Farkhod", 2.0),
    ("Attiks", 2.0),
    ("Riyad", 2.0),
    ("Salieva", 2.0),
    ("Karnazh", 2.0),
    ("Rigel", 2.0),
    ("Nega", 2.0),
    ("Arthurito", 2.0),
    ("Nscoder", 2.0),
    ("Muraking", 2.0),
    ("Sapphire", 2.0),
    ("Andrii", 2.0),
    ("Andrii mini", 10.0),
]

NAMES = [n for n, w in NAMES_WEIGHTS]
WEIGHTS = [w for n, w in NAMES_WEIGHTS]


def get_daily_name(user_id):
    today = datetime.now(KYIV_TZ).strftime("%Y-%m-%d")
    seed = int(hashlib.md5(f"{user_id}-{today}".encode()).hexdigest(), 16)
    rng = random.Random(seed)
    return rng.choices(NAMES, weights=WEIGHTS, k=1)[0]


async def start(update, context):
    await update.message.reply_text("Напиши @gvardiolhelperbot в любом чате чтобы узнать кто ты сегодня 👤")


async def inline_query(update, context):
    user_id = update.inline_query.from_user.id
    daily_name = get_daily_name(user_id)
    results = [
        InlineQueryResultPhoto(
            id=str(uuid.uuid4()),
            photo_url=PHOTO_URL,
            thumbnail_url=PHOTO_URL,
            title=" ",
            caption=f"Сегодня я *{daily_name}*",
            parse_mode="Markdown",
        )
    ]
    await update.inline_query.answer(results, cache_time=0)


if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(InlineQueryHandler(inline_query))
    print("gvardiolhelperbot запущен! ✅")
    app.run_polling()
