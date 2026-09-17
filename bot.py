import os
from urllib.parse import quote

from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)


# ============================================================
# ЗМІННІ СЕРЕДОВИЩА
# ============================================================

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TELEGRAM_BOT_TOKEN:
    raise RuntimeError(
        "TELEGRAM_BOT_TOKEN не знайдено. Перевір файл .env"
    )


# ============================================================
# ПОСИЛАННЯ
# ============================================================

TATTOO_FLASH_URL = (
    "https://www.tattooschool.in.ua/flash-tattoo/"
    "#ts-price-gallery-title"
)

COURSES_URL = "https://www.tattooschool.in.ua/courses/"

ADMIN_USERNAME = "tattooskool"

BOOKING_URL = f"https://t.me/{ADMIN_USERNAME}"


# ============================================================
# ПОСИЛАННЯ ДЛЯ ЗВ'ЯЗКУ З АДМІНІСТРАТОРОМ
# ============================================================

def create_admin_link(message: str) -> str:
    """
    Створює посилання на Telegram адміністратора
    з попередньо підготовленим повідомленням.
    """

    encoded_message = quote(message, safe="")

    return (
        f"https://t.me/{ADMIN_USERNAME}"
        f"?text={encoded_message}"
    )


START_CONTACT_URL = create_admin_link(
    "Добрий день! Мене цікавить курс START. "
    "Підкажіть, будь ласка, деталі та як можна записатися?"
)

PRO_CONTACT_URL = create_admin_link(
    "Добрий день! Мене цікавить курс PRO. "
    "Підкажіть, будь ласка, деталі та як можна записатися?"
)

EXPERT_CONTACT_URL = create_admin_link(
    "Добрий день! Мене цікавить курс EXPERT. "
    "Підкажіть, будь ласка, деталі та як можна записатися?"
)


# ============================================================
# ТЕКСТИ
# ============================================================

WELCOME_TEXT = """
<b>Вітаємо у Tattoo School 👋</b>

Оберіть напрямок:
"""


TATTOO_TEXT = """
<b>Тату</b>

Оберіть потрібний розділ:
"""


# ============================================================
# АКАДЕМІЯ
# ============================================================

ACADEMY_TEXT = """
<b>Курси Tattoo School 🎓</b>

Оберіть програму:
"""


COURSE_START_TEXT = f"""
<b>START — почати з нуля</b>

Опанувати професію та почати працювати тату-майстром.

<b>25 000 грн · 1,5 місяця</b>

Хочете дізнатися більше або записатися на курс?
{COURSES_URL}
Напишіть адміністратору 👇
"""


COURSE_PRO_TEXT = f"""
<b>PRO — стати сильним майстром</b>

Вдосконалити техніку, роботу з клієнтами та професійний рівень.

<b>36 000 грн · 2 місяці</b>

Хочете дізнатися більше або записатися на курс?
{COURSES_URL}
Напишіть адміністратору 👇
"""


COURSE_EXPERT_TEXT = f"""
<b>EXPERT — побудувати кар'єру</b>

Максимальна програма для тих, хто хоче розвиватися як майстер,
розвивати особистий бренд і рухатися до власної студії.

<b>45 000 грн · 2,5 місяця</b>

Хочете дізнатися більше або записатися на курс?
{COURSES_URL}
Напишіть адміністратору 👇
"""


# ============================================================
# ГОЛОВНЕ МЕНЮ
# ============================================================

def main_menu_keyboard():

    keyboard = [
        [
            InlineKeyboardButton(
                "🎓 Академія",
                callback_data="academy"
            )
        ],
        [
            InlineKeyboardButton(
                "🎨 Тату",
                callback_data="tattoo"
            )
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


# ============================================================
# МЕНЮ ТАТУ
# ============================================================

def tattoo_keyboard():

    keyboard = [
        [
            InlineKeyboardButton(
                "🎨 Переглянути ескізи",
                url=TATTOO_FLASH_URL
            )
        ],
        [
            InlineKeyboardButton(
                "📝 Записатися",
                url=BOOKING_URL
            )
        ],
        [
            InlineKeyboardButton(
                "⬅️ Назад",
                callback_data="main_menu"
            )
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


# ============================================================
# МЕНЮ АКАДЕМІЇ
# ============================================================

def academy_keyboard():

    keyboard = [
        [
            InlineKeyboardButton(
                "START — 25 000 грн ➡️",
                callback_data="course_start"
            )
        ],
        [
            InlineKeyboardButton(
                "PRO — 36 000 грн ➡️",
                callback_data="course_pro"
            )
        ],
        [
            InlineKeyboardButton(
                "EXPERT — 45 000 грн ➡️",
                callback_data="course_expert"
            )
        ],
        [
            InlineKeyboardButton(
                "⬅️ Назад",
                callback_data="main_menu"
            )
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


# ============================================================
# КНОПКИ КУРСІВ
# ============================================================

def course_keyboard(contact_url: str):

    keyboard = [
        [
            InlineKeyboardButton(
                "💬 Написати адміністратору",
                url=contact_url
            )
        ],
        [
            InlineKeyboardButton(
                "⬅️ До курсів",
                callback_data="academy"
            )
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


# ============================================================
# КОМАНДА /START
# ============================================================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if update.message is None:
        return

    await update.message.reply_text(
        WELCOME_TEXT,
        reply_markup=main_menu_keyboard(),
        parse_mode=ParseMode.HTML
    )


# ============================================================
# ОБРОБНИК КНОПОК
# ============================================================

async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    if query is None:
        return

    await query.answer()

    data = query.data


    # ========================================================
    # ГОЛОВНЕ МЕНЮ
    # ========================================================

    if data == "main_menu":

        text = WELCOME_TEXT
        keyboard = main_menu_keyboard()


    # ========================================================
    # ТАТУ
    # ========================================================

    elif data == "tattoo":

        text = TATTOO_TEXT
        keyboard = tattoo_keyboard()


    # ========================================================
    # АКАДЕМІЯ
    # ========================================================

    elif data == "academy":

        text = ACADEMY_TEXT
        keyboard = academy_keyboard()


    # ========================================================
    # КУРС START
    # ========================================================

    elif data == "course_start":

        text = COURSE_START_TEXT
        keyboard = course_keyboard(
            START_CONTACT_URL
        )


    # ========================================================
    # КУРС PRO
    # ========================================================

    elif data == "course_pro":

        text = COURSE_PRO_TEXT
        keyboard = course_keyboard(
            PRO_CONTACT_URL
        )


    # ========================================================
    # КУРС EXPERT
    # ========================================================

    elif data == "course_expert":

        text = COURSE_EXPERT_TEXT
        keyboard = course_keyboard(
            EXPERT_CONTACT_URL
        )


    # ========================================================
    # НЕВІДОМА КНОПКА
    # ========================================================

    else:
        return


    await query.edit_message_text(
        text,
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML
    )


# ============================================================
# ЗАПУСК БОТА
# ============================================================

def main():

    app = (
        Application.builder()
        .token(TELEGRAM_BOT_TOKEN)
        .build()
    )

    # Команда /start
    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    # Кнопки
    app.add_handler(
        CallbackQueryHandler(
            button_handler
        )
    )

    print("")
    print("================================")
    print("✅ Tattoo School Bot запущено")
    print("================================")
    print("")
    print("Натисніть Ctrl+C, щоб зупинити бота.")
    print("")

    app.run_polling()


# ============================================================
# START
# ============================================================

if __name__ == "__main__":
    main()
