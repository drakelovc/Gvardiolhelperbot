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
OWNER_USERNAME = "@drakelovc"
owner_chat_id = 6163072393

MAX_USES_PER_DAY = 3

# ── Чемпионы Гвардиолыча (с весами) ──────────────────────────────────────────
CHAMPIONS_WEIGHTS = [
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
CHAMPION_NAMES = [n for n, w in CHAMPIONS_WEIGHTS]
CHAMPION_WEIGHTS = [w for n, w in CHAMPIONS_WEIGHTS]

# ── Участники турнира (с описаниями) ─────────────────────────────────────────
PARTICIPANTS = {
    "))))))": "Душа компании, всегда приветствует всех",
    "-BMW M5 F90-": "Оценивает составы и ищет соперников",
    "333 Faret": "Новичок который сразу стал своим",
    "7": "Говорит мало, но метко",
    "8🩸": "Новый, но уже освоился в чате",
    "Accaman": "Всегда в деле, играет в нескольких турнирах",
    "Andrii": "Опытный участник, знает все про турниры",
    "Anton": "Фанат легендарных составов и карточек",
    "Atiks": "Считает себя лучшим в ФК Мобайл",
    "BRAZIL🇧🇷": "Любит Бразилию и всё бразильское",
    "Bastiano 🐾": "Всегда готов сыграть и скинуть результат",
    "CRIRO7": "Верный фанат Реал Мадрида и Роналдо",
    "Cr₽21": "Просит принять в лигу, но уже стал своим",
    "Denis": "Организованный — всегда следит за расписанием",
    "Diyorbek Turgunov": "Всегда приветливый и следит за жеребьёвкой",
    "Dmytro": "Новичок который сразу разобрался в правилах",
    "Doue": "Немногословный, но всегда в теме",
    "Drake": "Всегда в курсе событий турнира",
    "ELLIOT": "Тихий наблюдатель который знает что делает",
    "Emil Makulov": "Шатается во всех играх, но не унывает",
    "Farhod": "Всегда извиняется но играет до конца",
    "Grafs": "Любит легенды и разбирается в физических характеристиках",
    "Hhh": "Объясняет как работает система очков в лиге",
    "ItzRealMe": "Нежно кусается и всегда сам приходит",
    "Kaef": "Следит за правилами насчёт игроков в клубах",
    "L1r0rs": "Краткий и загадочный участник турнира",
    "Le": "Фанат Аль Насра и нестандартных джокеров",
    "Li Chi": "Всегда ждёт подтверждения начала турика",
    "M21": "Ищет соперников в группе ада",
    "Makarol": "Вечно спрашивает когда турнир и просит юз",
    "Makson": "Шутник который торгуется на миллиарды",
    "Me+Me": "Следит за экономикой и радуется редким картам",
    "Neymar": "Немногословный — приветствует и слушает",
    "Nikita": "Отвечает коротко: ура, пасиба, нет",
    "Oliver Queen": "Болельщик APL с вопросами про турнирную сетку",
    "Paduev": "Спрашивает как контрить Салибу на угловых",
    "Pavel Mametyev": "Говорит прямо и не терпит хуйни",
    "Petr": "Советует всем собирать состав в renderz",
    "Phoenileo": "Нервничает и трясётся перед каждым матчем",
    "Rigel": "Предлагает улучшения организации турнира",
    "Sapphire": "Желает удачи всем и болеет за Вест Хэм",
    "Shahruh": "Следит за всеми и жалеет участников",
    "Stepan": "Сразу признаётся что просрал",
    "Timur": "Просит принять в турнир вежливо",
    "VensanKompani": "Переживает за друга и следит за квестами лиги",
    "Vitaly": "Болеет за Францию во всех матчах",
    "Woody": "Сигма, всегда ищет игру в 4м слоте",
    "Yureeeec": "Анализирует сетку и следит за своей позицией",
    "ars.st": "Загадочный — только юз и минимум слов",
    "hsydnal": "Новичок который хотел зарегаться на турнир",
    "khaidarovw": "Следит за жеребьёвкой и турами",
    "kib": "Знает базы и разбирается в игре",
    "london": "Аналитик — предсказывает все счета матчей",
    "maybe": "Неопределённый — может залечь, а может и нет",
    "nscoder": "Миллионер турнира с нулевым смещением",
    "ohh": "Просит принять — и стал частью команды",
    "r1f_gaaaaz": "Всегда спрашивает как участвовать и когда новый",
    "rOmaa": "Sigma United с 80 миллионами бюджета",
    "riwuxe": "Считает жетоны и возмущается когда мало дают",
    "Ёжик🦔🔥": "Всегда готов сыграть прямо сейчас",
    "Абдулвохид": "Вежливый новичок который хочет попасть в турнир",
    "Александр": "Готов заменить любого с бюджетом 200 млн",
    "Александр Суворов": "Бавария — следит за таймингами событий",
    "Андрей": "Следит за всеми матчами Бенфики и Баварии",
    "Антон": "Готов заменить любого кто не придёт на игру",
    "Артем З": "Тихий участник с большими планами",
    "Белка": "Мечтает о Бразилии или Франции в составе",
    "Божен": "Фанат Реала с 2007 года — знает всё",
    "Ва Дим": "Загадочный — отвечает вопросом на вопрос",
    "Вадим": "Попал в бан но продолжает участвовать",
    "Валера": "Новенький который сразу стал активным",
    "ВоЛшЕбНиК": "Специалист по матчам со Словенией",
    "Гавитос": "Миллиардер турнира — бюджет 1ккк",
    "Даниил Алонсо": "Нашёл турнир на ютубе и сразу зарегался",
    "Данил": "Просит оценить состав за 20 миллионов",
    "Даня": "Всегда ждёт и уточняет правила сборки",
    "Дима": "Знает всех участников и называет их ники",
    "Дмитрий Пчельников": "Не может найти фильтр на рынке",
    "Егор": "Пиарит турнир и следит за своей группой",
    "Енот": "Жалеет что не участвует — хотел Германию 2014",
    "КИРИЛЛ": "Считает что за ПЗ платят слишком много",
    "Казимір Богдан": "Новенький агент который быстро освоился",
    "Лепс": "Активный — ждёт турнир и хочет быть тренером",
    "Максим": "Из лиги Гвардиолыча — собирал Барсу",
    "Марат Муратбеков": "Следит за всеми международными матчами",
    "Муся": "Играет за Польшу и всегда на завтра",
    "Назар": "Новенький которого путают с кем-то другим",
    "Нгумоха": "Пробует сложные составы несмотря на проблемы",
    "Нуралы": "Играет за испанские клубы в лиге",
    "Нурс": "Поздравляет победителей и уточняет регистрацию",
    "Паша": "Организатор группы 7 — созывает всех",
    "Пупсич": "Запутался куда писать ник но разобрался",
    "Салфетка 5": "Спрашивает совет по составу за 550 млн",
    "Сергей": "Советует брать Словакию — проверено чемпионами",
    "Стёпик": "Болельщик который ждёт не матч а драку",
    "Франсузик": "Аналитик — предсказывает каждый матч Австрии",
    "Хикматилло": "Вежливо спрашивает есть ли место в турнире",
    "артем": "Знаток составов и сборных",
    "найс": "Философ турнира — анализирует каждый момент",
    "ноуз": "Эксперт по редким картам и багоюзерам",
    "тимофей": "Новичок который пришёл и сразу выигрывал 2:0",
    "щищь": "Ищет отзывы про карточку Окочея 104",
    "янᴋᴇ": "Всегда анлак — Пикфорд съел что-то не то",
}

# ── Счётчики использования (турнир) ──────────────────────────────────────────
usage = {}


def get_today():
    return datetime.now(KYIV_TZ).strftime("%Y-%m-%d")


def can_use(user_id):
    today = get_today()
    if user_id not in usage or usage[user_id]["date"] != today:
        usage[user_id] = {"date": today, "count": 0}
    return usage[user_id]["count"] < MAX_USES_PER_DAY


def use_once(user_id):
    today = get_today()
    if user_id not in usage or usage[user_id]["date"] != today:
        usage[user_id] = {"date": today, "count": 0}
    usage[user_id]["count"] += 1


def get_remaining(user_id):
    today = get_today()
    if user_id not in usage or usage[user_id]["date"] != today:
        return MAX_USES_PER_DAY
    return MAX_USES_PER_DAY - usage[user_id]["count"]


# ── Логика чемпионов ──────────────────────────────────────────────────────────
def get_daily_champion(user_id):
    today = get_today()
    seed = int(hashlib.md5(f"{user_id}-{today}".encode()).hexdigest(), 16)
    rng = random.Random(seed)
    return rng.choices(CHAMPION_NAMES, weights=CHAMPION_WEIGHTS, k=1)[0]


def is_bonus_hunt():
    return random.random() < 0.005


# ── Хендлеры ─────────────────────────────────────────────────────────────────
async def start(update, context):
    global owner_chat_id
    user = update.effective_user
    if user.username and user.username.lower() == "drakelovc":
        owner_chat_id = update.effective_chat.id
        await update.message.reply_text("Привет! Ты сохранён как владелец бота ✅")
    else:
        await update.message.reply_text(
            "Напиши @gvardiolhelperbot в любом чате 👤\n"
            "Выбери одну из двух плашек:\n"
            "🏆 Кто ты среди чемпионов Гвардиолыча\n"
            "⚽ Кто ты из турнира Гвардиолыча"
        )


async def pravka(update, context):
    user = update.effective_user
    text = " ".join(context.args)
    if not text:
        await update.message.reply_text(
            "✏️ Напиши правку так:\n/pravka Найс — главный спамер чата"
        )
        return
    username = f"@{user.username}" if user.username else user.first_name
    await context.bot.send_message(
        chat_id=owner_chat_id,
        text=f"📝 Правка от {username}:\n{text}"
    )
    await update.message.reply_text("✅ Правка отправлена! Спасибо.")


async def resetme(update, context):
    user = update.effective_user
    if not (user.username and user.username.lower() == "drakelovc"):
        return  # тихо игнорируем для всех кроме владельца
    user_id = user.id
    usage[user_id] = {"date": get_today(), "count": 0}
    await update.message.reply_text("✅ Счётчик сброшен!")


async def inline_query(update, context):
    user_id = update.inline_query.from_user.id
    username = update.inline_query.from_user.username or "неизвестный"

    # ── Плашка 1: Чемпионы Гвардиолыча ──
    champion_name = get_daily_champion(user_id)
    bonus = is_bonus_hunt()

    if bonus:
        champion_text = f"Сегодня я *{champion_name}*\n\n🎉 *БОНУС ХАНТ!* Напиши @drakelovc чтобы получить подарок!"
        if owner_chat_id:
            try:
                await context.bot.send_message(
                    chat_id=owner_chat_id,
                    text=f"🎉 *БОНУС ХАНТ!*\nПользователь @{username} выиграл бонус!\nЕго ник сегодня: *{champion_name}*",
                    parse_mode="Markdown"
                )
            except Exception:
                pass
    else:
        champion_text = f"Сегодня я *{champion_name}*"

    card_champion = InlineQueryResultArticle(
        id=str(uuid.uuid4()),
        title="🏆 Кто ты среди чемпионов Гвардиолыча?",
        description="Нажми чтобы узнать своего чемпиона",
        thumbnail_url=PHOTO_URL,
        thumbnail_width=64,
        thumbnail_height=64,
        input_message_content=InputTextMessageContent(
            message_text=champion_text,
            parse_mode="Markdown",
        ),
    )

    # ── Плашка 2: Турнир Гвардиолыча ──
    if not can_use(user_id):
        card_tournament = InlineQueryResultArticle(
            id=str(uuid.uuid4()),
            title="⚽ Кто ты из турнира Гвардиолыча?",
            description="❌ Лимит исчерпан — попробуй завтра",
            thumbnail_url=PHOTO_URL,
            thumbnail_width=64,
            thumbnail_height=64,
            input_message_content=InputTextMessageContent(
                message_text="❌ Я уже использовал все 3 попытки! Попробуй завтра 🔄",
            ),
        )
    else:
        name, desc = random.choice(list(PARTICIPANTS.items()))
        use_once(user_id)
        remaining = get_remaining(user_id)
        bonus_tournament = is_bonus_hunt()
        if bonus_tournament:
            tournament_text = f"Сегодня я <b>{name}</b>\n<i>{desc}</i>\n\n🎉 <b>БОНУС ХАНТ!</b> Напиши <a href=\"https://t.me/drakelovc\">@drakelovc</a> чтобы получить подарок!\n<i>(осталось попыток: {remaining}/3)</i>"
            if owner_chat_id:
                try:
                    await context.bot.send_message(
                        chat_id=owner_chat_id,
                        text=f"🎉 *БОНУС ХАНТ!* (турнир)\nПользователь @{username} выиграл бонус!\nЕго участник сегодня: *{name}*",
                        parse_mode="Markdown"
                    )
                except Exception:
                    pass
        else:
            tournament_text = f"Сегодня я <b>{name}</b>\n<i>{desc}</i>\n\n<tg-spoiler>💡 Хочешь изменить описание? Напиши /pravka боту <a href=\"https://t.me/gvardiolhelperbot\">@gvardiolhelperbot</a></tg-spoiler>\n<i>(осталось попыток: {remaining}/3)</i>"
        card_tournament = InlineQueryResultArticle(
            id=str(uuid.uuid4()),
            title="⚽ Кто ты из турнира Гвардиолыча?",
            description="Нажми чтобы узнать своего участника",
            thumbnail_url=PHOTO_URL,
            thumbnail_width=64,
            thumbnail_height=64,
            input_message_content=InputTextMessageContent(
                message_text=tournament_text,
                parse_mode="HTML",
            ),
        )

    await update.inline_query.answer([card_champion, card_tournament], cache_time=0)


if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("pravka", pravka))
    app.add_handler(CommandHandler("resetme", resetme))
    app.add_handler(InlineQueryHandler(inline_query))
    print("gvardiolhelperbot запущен! ✅")
    app.run_polling()
