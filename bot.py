import random
import hashlib
from datetime import datetime
from zoneinfo import ZoneInfo
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ApplicationBuilder, CommandHandler, InlineQueryHandler, ContextTypes
import uuid

BOT_TOKEN = "8790414747:AAG5qfKOBs6J_oHIBBNTVnzNYkY9ioCxVn0"
PHOTO_URL = "https://i.ibb.co/ZzpdLzjj/Untitled101-20260403002828.png"
KYIV_TZ = ZoneInfo("Europe/Kyiv")

# Твой Telegram ID (получить можно через @userinfobot)
OWNER_USERNAME = "@drakelovc"

NAMES_WEIGHTS = [
    ("Freshl", 0.5),
    ("Anton", 0.7),
    ("Yurets", 1.0),
    ("Drake", 2.0),
    ("Dranniy", 2.0),
    ("Nurs", 1.5),
    ("Zenox", 1.5),
    ("Bagrat", 1.5),
    ("Vadim", 1.5),
    ("Nurali", 1.5),
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
    ("Andrii mini", 30.0),
]

NAMES = [n for n, w in NAMES_WEIGHTS]
WEIGHTS = [w for n, w in NAMES_WEIGHTS]

# Храним chat_id владельца
owner_chat_id = 6163072393


def get_daily_name(user_id):
    today = datetime.now(KYIV_TZ).strftime("%Y-%m-%d")
    seed = int(hashlib.md5(f"{user_id}-{today}".encode()).hexdigest(), 16)
    rng = random.Random(seed)
    return rng.choices(NAMES, weights=WEIGHTS, k=1)[0]


def is_bonus_hunt():
    # 0.5% шанс
    return random.random() < 0.005


async def start(update, context):
    global owner_chat_id
    user = update.effective_user
    # Сохраняем chat_id владельца автоматически
    if user.username and user.username.lower() == "drakelovc":
        owner_chat_id = update.effective_chat.id
        await update.message.reply_text("Привет! Ты сохранён как владелец бота ✅")
    else:
        await update.message.reply_text("Напиши @gvardiolhelperbot в любом чате чтобы узнать кто ты сегодня 👤")


async def inline_query(update, context):
    user_id = update.inline_query.from_user.id
    username = update.inline_query.from_user.username or "неизвестный"
    name = get_daily_name(user_id)
    bonus = is_bonus_hunt()

    if bonus:
        message_text = f"Сегодня я *{name}*\n\n🎉 *БОНУС ХАНТ!* Напиши @drakelovc чтобы получить подарок!"
        # Уведомляем владельца
        if owner_chat_id:
            try:
                await context.bot.send_message(
                    chat_id=owner_chat_id,
                    text=f"🎉 *БОНУС ХАНТ!*\nПользователь @{username} выиграл бонус!\nЕго ник сегодня: *{name}*",
                    parse_mode="Markdown"
                )
            except Exception:
                pass
    else:
        message_text = f"Сегодня я *{name}*"

    results = [
        InlineQueryResultArticle(
            id=str(uuid.uuid4()),
            title="Кто ты сегодня?",
            description="Нажми чтобы узнать",
            thumbnail_url=PHOTO_URL,
            thumbnail_width=64,
            thumbnail_height=64,
            input_message_content=InputTextMessageContent(
                message_text=message_text,
                parse_mode="Markdown",
            ),
        )
    ]
    await update.inline_query.answer(results, cache_time=0)


if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(InlineQueryHandler(inline_query))
    print("gvardiolhelperbot запущен! ✅")
    app.run_polling()
