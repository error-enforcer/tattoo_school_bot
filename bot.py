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

    encoded_message = quote(message)

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


PIERCING_TEXT = """
<b>Пірсинг</b>

Оберіть потрібний розділ:
"""


# ============================================================
# ПРАЙС НА ПІРСИНГ
# ============================================================

PIERCING_PRICES_TEXT = """
<b>Пірсинг — ціни</b>

<b>Позначення:</b>
• Без прикраси
• Мед. сталь — прокол + прикраса з медичної сталі
• Титан — прокол + титанова прикраса


<b>Мочка (Lobe)</b>
Без прикраси: 500 грн
Мед. сталь: 600 грн
Титан: 650 грн

<b>Дві мочки (Both Lobes)</b>
Без прикраси: 850 грн
Мед. сталь: 1050 грн
Титан: 1150 грн

<b>Helix / Scapha / Anti-Tragus</b>
Хелікс, анти-хелікс, хрящ вуха
Без прикраси: 550 грн
Мед. сталь: 650 грн
Титан: 700 грн

<b>Industrial / Orbital</b>
Індастріал
Без прикраси: 600 грн
Мед. сталь: 750 грн
Титан: 850 грн

<b>Tragus / Anti-Tragus</b>
Трагус, козелок, анти-трагус
Без прикраси: 550 грн
Мед. сталь: 650 грн
Титан: 700 грн

<b>Rook / Diath / Snug / Conch / Ragnar / Inner Pinna</b>
Без прикраси: 550 грн
Мед. сталь: 650 грн
Титан: 700 грн

<b>Nostril</b>
Крило носа
Без прикраси: 550 грн
Мед. сталь: 650 грн
Титан: 700 грн

<b>Septum / Nasallang</b>
Септум
Без прикраси: 550 грн
Мед. сталь: 650 грн
Титан: 700 грн

<b>Erl / Bridge / Third Eye</b>
Перенісся
Без прикраси: 550 грн
Мед. сталь: 650 грн
Титан: 700 грн

<b>Lip / Labret / Monroe / Medusa / Madonna</b>
Губа знизу / губа зверху
Без прикраси: 550 грн
Мед. сталь: 650 грн
Титан: 700 грн

<b>Snake / Spider / Angel Bites</b>
Подвійний прокол губи
Без прикраси: 1100 грн
Мед. сталь: 1300 грн
Титан: 1400 грн

<b>Lip Frenum / Frowny</b>
Смайл / анти-смайл
Без прикраси: 550 грн
Мед. сталь: 650 грн
Титан: 700 грн

<b>Tongue / Symmetric Tongue / Frenulum</b>
Язик / вуздечка язика
Без прикраси: 550 грн
Мед. сталь: 650 грн
Титан: 700 грн

<b>Антиброва</b>
Мед. сталь: 950 грн
Титан: 1000 грн

<b>Сосок (Nipple)</b>
Без прикраси: 750 грн
Титан: 900 грн

<b>Два соски (Both Nipples)</b>
Титан: 1700 грн

<b>Navel</b>
Вертикальний прокол пупка
Без прикраси: 550 грн
Мед. сталь: 650 грн
Титан: 700 грн

<b>Eyebrow / Anti-Eyebrow / Eyelid</b>
Брова
Без прикраси: 550 грн
Мед. сталь: 650 грн
Титан: 700 грн

<b>Інтимний пірсинг — жіночий</b>
Без прикраси: 1200 грн
Титан: 1400 грн

<b>Інтимний пірсинг — чоловічий</b>
Без прикраси: 1400 грн
Титан: 1500 грн

<b>Мікродермал / Dermal Anchor</b>
Без прикраси: 850 грн
Титан: 950 грн

<b>Розтягування тунелів 4–10 мм</b>
Без прикраси: 850 грн
Титан: 1000 грн


<b>Додаткові послуги</b>

• Заміна прикраси — від 100 грн
• Чищення проколу (крім мікродермала) — 250 грн
• Заміна накрутки мікродермалу — 300 грн
• Чищення та видалення мікродермалу — 350 грн
• Знеболення (аплікація TKTX) — 100 грн
"""


# ============================================================
# АКАДЕМІЯ
# ============================================================

ACADEMY_TEXT = """
<b>Курси Tattoo School 🎓</b>

Оберіть програму:
"""


COURSE_START_TEXT = """
<b>START — почати з нуля</b>

Опанувати професію та почати працювати тату-майстром.

<b>25 000 грн · 1,5 місяця</b>

Хочете дізнатися більше або записатися на курс?
Напишіть адміністратору 👇
"""


COURSE_PRO_TEXT = """
<b>PRO — стати сильним майстром</b>

Вдосконалити техніку, роботу з клієнтами та професійний рівень.

<b>36 000 грн · 2 місяці</b>

Хочете дізнатися більше або записатися на курс?
Напишіть адміністратору 👇
"""


COURSE_EXPERT_TEXT = """
<b>EXPERT — побудувати кар'єру</b>

Максимальна програма для тих, хто хоче розвиватися як майстер, розвивати особистий бренд і рухатися до власної студії.

<b>45 000 грн · 2,5 місяця</b>

Хочете дізнатися більше або записатися на курс?
Напишіть адміністратору 👇
"""


# ============================================================
# ГОЛОВНЕ МЕНЮ
# ============================================================

def main_menu_keyboard():

    keyboard = [
        [
            InlineKeyboardButton(
                "🎨 Тату",
                callback_data="tattoo"
            )
        ],
        [
            InlineKeyboardButton(
                "✨ Пірсинг",
                callback_data="piercing"
            )
        ],
        [
            InlineKeyboardButton(
                "🎓 Академія",
                callback_data="academy"
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
# МЕНЮ ПІРСИНГУ
# ============================================================

def piercing_keyboard():

    keyboard = [
        [
            InlineKeyboardButton(
                "💰 Переглянути ціни",
                callback_data="piercing_prices"
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


def back_to_piercing_keyboard():

    keyboard = [
        [
            InlineKeyboardButton(
                "📝 Записатися на пірсинг",
                url=BOOKING_URL
            )
        ],
        [
            InlineKeyboardButton(
                "⬅️ До пірсингу",
                callback_data="piercing"
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
                "START — 25 000 грн",
                callback_data="course_start"
            )
        ],
        [
            InlineKeyboardButton(
                "PRO — 36 000 грн",
                callback_data="course_pro"
            )
        ],
        [
            InlineKeyboardButton(
                "EXPERT — 45 000 грн",
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
# КНОПКИ КУРСУ START
# ============================================================

def start_course_keyboard():

    keyboard = [
        [
            InlineKeyboardButton(
                "💬 Написати адміністратору",
                url=START_CONTACT_URL
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
# КНОПКИ КУРСУ PRO
# ============================================================

def pro_course_keyboard():

    keyboard = [
        [
            InlineKeyboardButton(
                "💬 Написати адміністратору",
                url=PRO_CONTACT_URL
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
# КНОПКИ КУРСУ EXPERT
# ============================================================

def expert_course_keyboard():

    keyboard = [
        [
            InlineKeyboardButton(
                "💬 Написати адміністратору",
                url=EXPERT_CONTACT_URL
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

    await query.answer()

    data = query.data


    # ========================================================
    # ГОЛОВНЕ МЕНЮ
    # ========================================================

    if data == "main_menu":

        await query.edit_message_text(
            WELCOME_TEXT,
            reply_markup=main_menu_keyboard(),
            parse_mode=ParseMode.HTML
        )


    # ========================================================
    # ТАТУ
    # ========================================================

    elif data == "tattoo":

        await query.edit_message_text(
            TATTOO_TEXT,
            reply_markup=tattoo_keyboard(),
            parse_mode=ParseMode.HTML
        )


    # ========================================================
    # ПІРСИНГ
    # ========================================================

    elif data == "piercing":

        await query.edit_message_text(
            PIERCING_TEXT,
            reply_markup=piercing_keyboard(),
            parse_mode=ParseMode.HTML
        )


    elif data == "piercing_prices":

        await query.edit_message_text(
            PIERCING_PRICES_TEXT,
            reply_markup=back_to_piercing_keyboard(),
            parse_mode=ParseMode.HTML
        )


    # ========================================================
    # АКАДЕМІЯ
    # ========================================================

    elif data == "academy":

        await query.edit_message_text(
            ACADEMY_TEXT,
            reply_markup=academy_keyboard(),
            parse_mode=ParseMode.HTML
        )


    # ========================================================
    # КУРС START
    # ========================================================

    elif data == "course_start":

        await query.edit_message_text(
            COURSE_START_TEXT,
            reply_markup=start_course_keyboard(),
            parse_mode=ParseMode.HTML
        )


    # ========================================================
    # КУРС PRO
    # ========================================================

    elif data == "course_pro":

        await query.edit_message_text(
            COURSE_PRO_TEXT,
            reply_markup=pro_course_keyboard(),
            parse_mode=ParseMode.HTML
        )


    # ========================================================
    # КУРС EXPERT
    # ========================================================

    elif data == "course_expert":

        await query.edit_message_text(
            COURSE_EXPERT_TEXT,
            reply_markup=expert_course_keyboard(),
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
