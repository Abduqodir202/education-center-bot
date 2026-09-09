import asyncio
import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.fsm.state import State, StatesGroup
from about.menu import router as about_router
from back.menu import router as back_router
from results.menu import router as results_router
from promotions.menu import router as promotions_router
from prices.menu import router as prices_router
from teachers.menu import router as teachers_router
from location.menu import router as location_router

from contact.menu import router as contact_router

from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    CallbackQuery,
    ReplyKeyboardRemove,
    InlineKeyboardMarkup,
)

from database import (
    create_database,
    save_application,
    update_application_status,
    get_applications,
    get_applications_by_status,
    # search_applications,
    get_statistics
)

from dotenv import load_dotenv

# 📚 Kurslar routeri
from courses.menu import router as courses_router


# =========================================================
# 🤖 BOT TOKEN
# =========================================================

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 7876153704
# ADMIN_ID = 6508834905

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN topilmadi! .env faylni tekshiring.")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# 📚 Kurslar routerini ulash
dp.include_router(about_router)
dp.include_router(courses_router)
dp.include_router(back_router)
dp.include_router(results_router)
dp.include_router(promotions_router)
dp.include_router(prices_router)
dp.include_router(teachers_router)
dp.include_router(location_router)
dp.include_router(contact_router)

# =========================================================
# FSM
# =========================================================

class Registration(StatesGroup):
    language = State()
    name = State()
    age = State()
    phone = State()
    location = State()
    subject = State()
    level = State()
    format = State()
    lesson_time = State()
    confirmation = State()


# =========================================================
# MATNLAR
# =========================================================

TEXTS = {
    "uz": {
        "welcome": (
            "🎓 ZAMON O‘QUV MARKAZI\n\n"
            "Assalomu alaykum! 👋\n\n"
            "Zamon o‘quv markazining rasmiy qabul botiga xush kelibsiz!\n\n"
            "📚 Ushbu bot orqali siz:\n"
            "• Kurslarni tanlashingiz\n"
            "• Bilim darajangizni belgilashingiz\n"
            "• Qulay dars vaqtini tanlashingiz\n"
            "• O‘qishga onlayn ariza qoldirishingiz mumkin.\n\n"
            "🚀 O‘qishni boshlash uchun tilni tanlang:"
        ),
        "name": "👤 Ismingizni kiriting:",
        "phone": "📱 Telefon raqamingizni yuboring:",
        "age": "🎂 Yoshingiz nechida?",
        "location": "📍 Qayerda yashaysiz?",
        "subject": "📚 Qaysi fanga qatnashmoqchisiz?",
        "level": "📊 Bilim darajangizni tanlang:",
        "format": "💻 Ta’lim shaklini tanlang:",
        "time": "🕐 Sizga qaysi dars vaqti qulay?",
        "confirm": "📋 Ma’lumotlaringizni tekshiring:\n\nHammasi to‘g‘rimi?",
        "confirmed": "✅ Arizangiz qabul qilindi!\n\nTez orada administrator siz bilan bog‘lanadi.",
        "cancelled": "❌ Ariza bekor qilindi.\n\nQaytadan boshlaymiz.",
        "error_age": "❗ Iltimos, yoshingizni raqam bilan kiriting.",
        "error_age_range": "❗ Iltimos, to‘g‘ri yosh kiriting.",
        "invalid_name": "❗ Iltimos, ismingizni kiriting.",
        "invalid_location": "❗ Iltimos, yashash joyingizni kiriting.",
    },
    "ru": {
        "welcome": (
            "🎓 ZAMON О‘QUV MARKAZI\n\n"
            "Здравствуйте! 👋\n\n"
            "Добро пожаловать в официальный бот учебного центра Zamon!\n\n"
            "📚 С помощью этого бота вы можете:\n"
            "• Выбрать курс\n"
            "• Указать свой уровень знаний\n"
            "• Выбрать удобное время занятий\n"
            "• Оставить заявку на обучение\n\n"
            "🚀 Для начала выберите язык:"
        ),
        "name": "👤 Введите ваше имя:",
        "phone": "📱 Отправьте ваш номер телефона:",
        "age": "🎂 Сколько вам лет?",
        "location": "📍 Где вы живёте?",
        "subject": "📚 Какой предмет вы хотите изучать?",
        "level": "📊 Выберите ваш уровень знаний:",
        "format": "💻 Выберите формат обучения:",
        "time": "🕐 Какое время занятий вам удобно?",
        "confirm": "📋 Проверьте ваши данные:\n\nВсё правильно?",
        "confirmed": "✅ Ваша заявка принята!\n\nСкоро администратор свяжется с вами.",
        "cancelled": "❌ Заявка отменена.\n\nНачнём заново.",
        "error_age": "❗ Пожалуйста, введите возраст цифрами.",
        "error_age_range": "❗ Пожалуйста, введите правильный возраст.",
        "invalid_name": "❗ Пожалуйста, введите ваше имя.",
        "invalid_location": "❗ Пожалуйста, укажите место проживания.",
    },
    "en": {
        "welcome": (
            "🎓 ZAMON EDUCATION CENTER\n\n"
            "Hello! 👋\n\n"
            "Welcome to the official Zamon Education Center registration bot!\n\n"
            "📚 With this bot you can:\n"
            "• Choose a course\n"
            "• Select your level\n"
            "• Choose a convenient lesson time\n"
            "• Submit an application for enrollment\n\n"
            "🚀 Choose your language to get started:"
        ),
        "name": "👤 Enter your name:",
        "phone": "📱 Send your phone number:",
        "age": "🎂 How old are you?",
        "location": "📍 Where do you live?",
        "subject": "📚 Which subject would you like to study?",
        "level": "📊 Choose your level:",
        "format": "💻 Choose your learning format:",
        "time": "🕐 What lesson time is convenient for you?",
        "confirm": "📋 Please check your information:\n\nIs everything correct?",
        "confirmed": "✅ Your application has been accepted!\n\nAn administrator will contact you soon.",
        "cancelled": "❌ Application cancelled.\n\nLet's start again.",
        "error_age": "❗ Please enter your age as a number.",
        "error_age_range": "❗ Please enter a valid age.",
        "invalid_name": "❗ Please enter your name.",
        "invalid_location": "❗ Please enter your location.",
    },
}


# =========================================================
# FANLAR
# =========================================================

SUBJECTS = {
    "uz": {
        "russian": "🇷🇺 Rus tili",
        "english": "🇬🇧 Ingliz tili",
        "math": "🧮 Matematika",
        "mental": "🧠 Mental arifmetika",
    },
    "ru": {
        "russian": "🇷🇺 Русский язык",
        "english": "🇬🇧 Английский язык",
        "math": "🧮 Математика",
        "mental": "🧠 Ментальная арифметика",
    },
    "en": {
        "russian": "🇷🇺 Russian",
        "english": "🇬🇧 English",
        "math": "🧮 Mathematics",
        "mental": "🧠 Mental arithmetic",
    },
}


# =========================================================
# BILIM DARAJASI
# =========================================================

LEVELS = {
    "uz": {
        "beginner": "🌱 Boshlang‘ich",
        "middle": "📚 O‘rta",
        "advanced": "🎓 Yuqori",
    },
    "ru": {
        "beginner": "🌱 Начальный",
        "middle": "📚 Средний",
        "advanced": "🎓 Продвинутый",
    },
    "en": {
        "beginner": "🌱 Beginner",
        "middle": "📚 Intermediate",
        "advanced": "🎓 Advanced",
    },
}


# =========================================================
# FORMAT
# =========================================================

FORMATS = {
    "uz": {
        "online": "💻 Online",
        "offline": "🏫 Offline",
    },
    "ru": {
        "online": "💻 Онлайн",
        "offline": "🏫 Офлайн",
    },
    "en": {
        "online": "💻 Online",
        "offline": "🏫 Offline",
    },
}


# =========================================================
# VAQTLAR
# =========================================================

TIMES = {
    "uz": {
        "09": "🕘 09:00 – 10:30",
        "11": "🕚 11:00 – 12:30",
        "14": "🕑 14:00 – 15:30",
        "17": "🕔 17:00 – 18:30",
        "19": "🕖 19:00 – 20:30",
    },
    "ru": {
        "09": "🕘 09:00 – 10:30",
        "11": "🕚 11:00 – 12:30",
        "14": "🕑 14:00 – 15:30",
        "17": "🕔 17:00 – 18:30",
        "19": "🕖 19:00 – 20:30",
    },
    "en": {
        "09": "🕘 09:00 – 10:30",
        "11": "🕚 11:00 – 12:30",
        "14": "🕑 14:00 – 15:30",
        "17": "🕔 17:00 – 18:30",
        "19": "🕖 19:00 – 20:30",
    },
}


# =========================================================
# NARX
# =========================================================

def calculate_price(age: int) -> int:
    if age < 14:
        return 300_000
    elif age < 18:
        return 400_000
    elif age <= 30:
        return 500_000
    else:
        return 600_000


# =========================================================
# START
# =========================================================

@dp.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    await state.clear()

    builder = InlineKeyboardBuilder()

    builder.button(
        text="📝 Ariza berish",
        callback_data="apply"
    )

    builder.button(
        text="📚 Kurslarimiz",
        callback_data="courses"
    )

    builder.button(
        text="🏢 Biz haqimizda",
        callback_data="about"
    )

    builder.button(
        text="👨‍🏫 Bizning ustozlar",
        callback_data="teachers"
    )

    builder.button(
        text="🏆 Bizning natijalar",
        callback_data="results"
    )

    builder.button(
        text="🎁 Aksiyalar va imtiyozlar",
        callback_data="promotions"
    )

    builder.button(
        text="💰 Kurs narxlari",
        callback_data="prices"
    )

    builder.button(
        text="📍 Bizning manzil",
        callback_data="location"
    )

    builder.button(
        text="📞 Biz bilan bog‘lanish",
        callback_data="contact"
    )

    builder.adjust(2)

    await message.answer(
        "🎓 <b>ZAMON O‘QUV MARKAZI</b>\n\n"
        "Assalomu alaykum! 👋\n\n"
        "Quyidagi bo‘limlardan birini tanlang:",
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )

# =========================================================
# 📝 ARIZA BERISH
# =========================================================

@dp.callback_query(F.data == "apply")
async def apply_handler(callback: CallbackQuery, state: FSMContext):

    builder = InlineKeyboardBuilder()

    builder.button(
        text="🇺🇿 O‘zbek tili",
        callback_data="uz"
    )

    builder.button(
        text="🇷🇺 Русский язык",
        callback_data="ru"
    )

    builder.button(
        text="🇬🇧 English",
        callback_data="en"
    )

    builder.adjust(1)

    await callback.message.edit_text(
        "🌐 Ariza to‘ldirish uchun tilni tanlang:",
        reply_markup=builder.as_markup()
    )

    # MUHIM!
    await state.set_state(Registration.language)

    await callback.answer()

# =========================================================
# TIL
# =========================================================

@dp.callback_query(Registration.language, F.data.in_({"uz", "ru", "en"}))
async def language_handler(callback: CallbackQuery, state: FSMContext):
    language = callback.data
    await state.update_data(language=language)

    await callback.message.edit_text(TEXTS[language]["name"])
    await state.set_state(Registration.name)
    await callback.answer()


# =========================================================
# ISM
# =========================================================

@dp.message(Registration.name)
async def name_handler(message: Message, state: FSMContext):
    if not message.text or not message.text.strip():
        data = await state.get_data()
        await message.answer(TEXTS[data["language"]]["invalid_name"])
        return

    await state.update_data(name=message.text.strip())
    data = await state.get_data()
    language = data["language"]

    builder = ReplyKeyboardBuilder()

    if language == "uz":
        button_text = "📱 Telefon raqamimni yuborish"
    elif language == "ru":
        button_text = "📱 Отправить мой номер"
    else:
        button_text = "📱 Send my phone number"

    builder.button(text=button_text, request_contact=True)
    builder.adjust(1)

    await message.answer(
        TEXTS[language]["phone"],
        reply_markup=builder.as_markup(
            resize_keyboard=True,
            one_time_keyboard=True,
        ),
    )

    await state.set_state(Registration.phone)


# =========================================================
# TELEFON
# =========================================================

@dp.message(Registration.phone, F.contact)
async def phone_handler(message: Message, state: FSMContext):
    phone = message.contact.phone_number
    await state.update_data(phone=phone)

    data = await state.get_data()
    language = data["language"]

    await message.answer(
        TEXTS[language]["age"],
        reply_markup=ReplyKeyboardRemove(),
    )

    await state.set_state(Registration.age)


@dp.message(Registration.phone)
async def invalid_phone_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    language = data["language"]

    await message.answer(TEXTS[language]["phone"])


# =========================================================
# YOSH
# =========================================================

@dp.message(Registration.age)
async def age_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    language = data["language"]

    try:
        age = int(message.text.strip())
    except (ValueError, AttributeError):
        await message.answer(TEXTS[language]["error_age"])
        return

    if age < 1 or age > 100:
        await message.answer(TEXTS[language]["error_age_range"])
        return

    await state.update_data(age=age)
    await message.answer(TEXTS[language]["location"])
    await state.set_state(Registration.location)


# =========================================================
# YASHASH JOYI
# =========================================================

@dp.message(Registration.location)
async def location_handler(message: Message, state: FSMContext):
    if not message.text or not message.text.strip():
        data = await state.get_data()
        await message.answer(TEXTS[data["language"]]["invalid_location"])
        return

    await state.update_data(location=message.text.strip())
    data = await state.get_data()
    language = data["language"]

    builder = InlineKeyboardBuilder()

    for code, name in SUBJECTS[language].items():
        builder.button(text=name, callback_data=f"subject_{code}")

    builder.adjust(1)

    await message.answer(
        TEXTS[language]["subject"],
        reply_markup=builder.as_markup(),
    )

    await state.set_state(Registration.subject)


# =========================================================
# FAN
# =========================================================

@dp.callback_query(Registration.subject, F.data.startswith("subject_"))
async def subject_handler(callback: CallbackQuery, state: FSMContext):
    subject = callback.data.replace("subject_", "", 1)
    await state.update_data(subject=subject)

    data = await state.get_data()
    language = data["language"]

    builder = InlineKeyboardBuilder()

    for code, name in LEVELS[language].items():
        builder.button(text=name, callback_data=f"level_{code}")

    builder.adjust(1)

    await callback.message.edit_text(
        TEXTS[language]["level"],
        reply_markup=builder.as_markup(),
    )

    await state.set_state(Registration.level)
    await callback.answer()


# =========================================================
# BILIM DARAJASI
# =========================================================

@dp.callback_query(Registration.level, F.data.startswith("level_"))
async def level_handler(callback: CallbackQuery, state: FSMContext):
    level = callback.data.replace("level_", "", 1)
    await state.update_data(level=level)

    data = await state.get_data()
    language = data["language"]

    # Faqat rus tili uchun Online / Offline tanlovi
    if data["subject"] == "russian":
        builder = InlineKeyboardBuilder()

        for code, name in FORMATS[language].items():
            builder.button(text=name, callback_data=f"format_{code}")

        builder.adjust(1)

        await callback.message.edit_text(
            TEXTS[language]["format"],
            reply_markup=builder.as_markup(),
        )

        await state.set_state(Registration.format)

    else:
        await show_time_buttons(callback.message, language, state)

    await callback.answer()


# =========================================================
# ONLINE / OFFLINE
# =========================================================

@dp.callback_query(Registration.format, F.data.startswith("format_"))
async def format_handler(callback: CallbackQuery, state: FSMContext):
    education_format = callback.data.replace("format_", "", 1)
    await state.update_data(format=education_format)

    data = await state.get_data()
    language = data["language"]

    await show_time_buttons(callback.message, language, state)
    await callback.answer()


# =========================================================
# VAQT TUGMALARI
# =========================================================

async def show_time_buttons(message: Message, language: str, state: FSMContext):
    builder = InlineKeyboardBuilder()

    for code, name in TIMES[language].items():
        builder.button(text=name, callback_data=f"time_{code}")

    builder.adjust(1)

    await message.edit_text(
        TEXTS[language]["time"],
        reply_markup=builder.as_markup(),
    )

    await state.set_state(Registration.lesson_time)


# =========================================================
# VAQT
# =========================================================

@dp.callback_query(Registration.lesson_time, F.data.startswith("time_"))
async def time_handler(callback: CallbackQuery, state: FSMContext):
    lesson_time = callback.data.replace("time_", "", 1)
    await state.update_data(lesson_time=lesson_time)

    data = await state.get_data()
    language = data["language"]

    # Narx
    if data["subject"] == "russian" and data.get("format") == "online":
        price = 200_000
    else:
        price = calculate_price(data["age"])

    # Format
    if data["subject"] == "russian":
        education_format = FORMATS[language][data["format"]]
    else:
        education_format = "🏫 Offline"

    subject = SUBJECTS[language][data["subject"]]
    level = LEVELS[language][data["level"]]
    time_name = TIMES[language][data["lesson_time"]]

    if language == "uz":
        price_text = f"💰 Narx: {price:,} so‘m"
        name_text = "👤 Ism"
        phone_text = "📱 Telefon"
        age_text = "🎂 Yosh"
        location_text = "📍 Manzil"
        subject_text = "📚 Fan"
        level_text = "📊 Daraja"
        format_text = "💻 Ta’lim shakli"
        time_text = "🕐 Dars vaqti"
    elif language == "ru":
        price_text = f"💰 Стоимость: {price:,} сум"
        name_text = "👤 Имя"
        phone_text = "📱 Телефон"
        age_text = "🎂 Возраст"
        location_text = "📍 Адрес"
        subject_text = "📚 Предмет"
        level_text = "📊 Уровень"
        format_text = "💻 Формат обучения"
        time_text = "🕐 Время занятий"
    else:
        price_text = f"💰 Price: {price:,} UZS"
        name_text = "👤 Name"
        phone_text = "📱 Phone"
        age_text = "🎂 Age"
        location_text = "📍 Location"
        subject_text = "📚 Subject"
        level_text = "📊 Level"
        format_text = "💻 Learning format"
        time_text = "🕐 Lesson time"

    result = (
        f"{TEXTS[language]['confirm']}\n\n"
        f"{name_text}: {data['name']}\n"
        f"{phone_text}: {data['phone']}\n"
        f"{age_text}: {data['age']}\n"
        f"{location_text}: {data['location']}\n"
        f"{subject_text}: {subject}\n"
        f"{level_text}: {level}\n"
    )

    if education_format:
        result += f"{format_text}: {education_format}\n"

    result += f"{price_text}\n{time_text}: {time_name}"

    builder = InlineKeyboardBuilder()

    if language == "uz":
        confirm_text = "✅ Tasdiqlash"
        cancel_text = "❌ Bekor qilish"
    elif language == "ru":
        confirm_text = "✅ Подтвердить"
        cancel_text = "❌ Отменить"
    else:
        confirm_text = "✅ Confirm"
        cancel_text = "❌ Cancel"

    builder.button(text=confirm_text, callback_data="confirm")
    builder.button(text=cancel_text, callback_data="cancel")
    builder.adjust(1)

    await callback.message.edit_text(
        result,
        reply_markup=builder.as_markup(),
    )

    await state.set_state(Registration.confirmation)
    await callback.answer()


# =========================================================
# TASDIQLASH
# =========================================================

@dp.callback_query(Registration.confirmation, F.data == "confirm")
async def confirm_handler(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    language = data["language"]

    # Narxni qayta hisoblaymiz
    if data["subject"] == "russian" and data.get("format") == "online":
        price = 200_000
    else:
        price = calculate_price(data["age"])

    subject = SUBJECTS[language][data["subject"]]
    level = LEVELS[language][data["level"]]
    time_name = TIMES[language][data["lesson_time"]]

    if data["subject"] == "russian":
        education_format = FORMATS[language][data["format"]]
    else:
        education_format = "🏫 Offline"

    # FAQAT TASDIQLANGANDAN KEYIN DATABASE'GA SAQLANADI
    application_id = await save_application(
        telegram_id=callback.from_user.id,
        username=callback.from_user.username,
        name=data["name"],
        phone=data["phone"],
        age=data["age"],
        location=data["location"],
        subject=data["subject"],
        level=data["level"],
        education_format=education_format,
        lesson_time=data["lesson_time"],
        price=price,
    )

    username = callback.from_user.username
    username_text = f"@{username}" if username else "Ko‘rsatilmagan"

    admin_message = (
        "🆕 YANGI O‘QUVCHI\n\n"
        f"🆔 Ariza ID: {application_id}\n\n"
        f"👤 Ism: {data['name']}\n"
        f"📱 Telefon: {data['phone']}\n"
        f"🎂 Yosh: {data['age']}\n"
        f"📍 Manzil: {data['location']}\n"
        f"📚 Fan: {subject}\n"
        f"📊 Daraja: {level}\n"
        f"💻 Ta’lim shakli: {education_format}\n"
        f"💰 Narx: {price:,} so‘m\n"
        f"🕐 Dars vaqti: {time_name}\n\n"
        f"🆔 Telegram ID: {callback.from_user.id}\n"
        f"👤 Username: {username_text}"
    )

    admin_builder = InlineKeyboardBuilder()

    admin_builder.button(
        text="📞 Bog‘lanildi",
        callback_data=f"admin_contacted:{application_id}",
    )
    admin_builder.button(
        text="✅ Qabul qilindi",
        callback_data=f"admin_accepted:{application_id}",
    )
    admin_builder.button(
        text="❌ Rad etildi",
        callback_data=f"admin_rejected:{application_id}",
    )
    admin_builder.adjust(1)

    # Adminga yuborish
    try:
        await bot.send_message(
            chat_id=ADMIN_ID,
            text=admin_message,
            reply_markup=admin_builder.as_markup(),
        )
    except Exception as e:
        print(f"Admin xabarini yuborishda xato: {e}")

    await callback.message.edit_text(
        TEXTS[language]["confirmed"]
    )

    await state.clear()
    await callback.answer()


# =========================================================
# BEKOR QILISH
# =========================================================

@dp.callback_query(Registration.confirmation, F.data == "cancel")
async def cancel_handler(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    language = data.get("language", "uz")

    builder = InlineKeyboardBuilder()
    builder.button(text="🇺🇿 O‘zbek tili", callback_data="uz")
    builder.button(text="🇷🇺 Русский язык", callback_data="ru")
    builder.button(text="🇬🇧 English", callback_data="en")
    builder.adjust(1)

    await callback.message.edit_text(
        TEXTS[language]["cancelled"]
        + "\n\n"
        + TEXTS[language]["welcome"],
        reply_markup=builder.as_markup(),
    )

    await state.set_state(Registration.language)
    await callback.answer()


# =========================================================
# ADMIN STATUSNI O‘ZGARTIRISH
# =========================================================

async def change_admin_status(
    callback: CallbackQuery,
    status: str,
    status_text: str,
    callback_prefix: str,
):
    if not callback.data or ":" not in callback.data:
        await callback.answer("❗ Ariza ID topilmadi.", show_alert=True)
        return

    application_id = callback.data.split(":", 1)[1]

    # Database statusini o‘zgartiramiz
    await update_application_status(application_id, status)

    text = callback.message.text or ""

    # Oldingi statusni tozalaymiz
    for old_status in (
        "\n\n📌 STATUS: 📞 Bog‘lanildi",
        "\n\n📌 STATUS: ✅ Qabul qilindi",
        "\n\n📌 STATUS: ❌ Rad etildi",
    ):
        text = text.replace(old_status, "")

    # Yangi statusni qo‘shamiz
    if "🆕 YANGI O‘QUVCHI" in text:
        text = text.replace(
            "🆕 YANGI O‘QUVCHI",
            f"🆕 YANGI O‘QUVCHI\n\n📌 STATUS: {status_text}",
            1,
        )

    # Faqat bosilgan tugmani o‘chiramiz
    keyboard = callback.message.reply_markup

    if keyboard:
        new_keyboard = []

        for row in keyboard.inline_keyboard:
            new_row = []

            for button in row:
                if button.callback_data == f"{callback_prefix}{application_id}":
                    continue

                new_row.append(button)

            if new_row:
                new_keyboard.append(new_row)

        keyboard = InlineKeyboardMarkup(inline_keyboard=new_keyboard)

    await callback.message.edit_text(
        text,
        reply_markup=keyboard,
    )

    await callback.answer(status_text)

# =========================================================
# ADMIN — STATISTIKA
# =========================================================

@dp.callback_query(F.data == "statistics")
async def statistics_handler(callback: CallbackQuery):

    if callback.from_user.id != ADMIN_ID:
        await callback.answer(
            "❌ Sizda ruxsat yo‘q.",
            show_alert=True
        )
        return

    stats = await get_statistics()

    text = (
        "📊 <b>STATISTIKA</b>\n\n"
        f"👥 <b>Jami arizalar:</b> {stats['total']}\n\n"
        f"🆕 <b>Yangi:</b> {stats['new']}\n"
        f"📞 <b>Bog‘lanilgan:</b> {stats['contacted']}\n"
        f"✅ <b>Qabul qilingan:</b> {stats['accepted']}\n"
        f"❌ <b>Rad etilgan:</b> {stats['rejected']}"
    )

    builder = InlineKeyboardBuilder()
    builder.button(text="⬅️ Orqaga", callback_data="applications_menu")
    builder.adjust(1)

    await callback.message.edit_text(
        text,
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )

    await callback.answer()


# =========================================================
# ADMIN — STATUS FILTER
# =========================================================

@dp.callback_query(
    F.data.startswith("filter:")
)
async def application_filter_handler(
        callback: CallbackQuery
):

    if callback.from_user.id != ADMIN_ID:
        await callback.answer(
            "❌ Sizda ruxsat yo‘q.",
            show_alert=True
        )
        return

    filter_status = callback.data.split(":")[1]

    if filter_status == "all":

        applications = await get_applications()

        title = "📋 BARCHA ARIZALAR"

    else:

        applications = await get_applications_by_status(
            filter_status
        )

        status_titles = {
            "new": "🆕 YANGI ARIZALAR",
            "contacted": "📞 BOG‘LANILGAN ARIZALAR",
            "accepted": "✅ QABUL QILINGAN ARIZALAR",
            "rejected": "❌ RAD ETILGAN ARIZALAR"
        }

        title = status_titles.get(
            filter_status,
            "📋 ARIZALAR"
        )

    if not applications:

        builder = InlineKeyboardBuilder()

        builder.button(
            text="⬅️ Orqaga",
            callback_data="applications_menu"
        )

        await callback.message.edit_text(
            f"<b>{title}</b>\n\n"
            "📭 Bu bo‘limda hozircha ariza yo‘q.",
            reply_markup=builder.as_markup(),
            parse_mode="HTML"
        )

        await callback.answer()
        return

    builder = InlineKeyboardBuilder()

    for app in applications:

        status = app["status"]

        if status == "new":
            icon = "🆕"
        elif status == "contacted":
            icon = "📞"
        elif status == "accepted":
            icon = "✅"
        elif status == "rejected":
            icon = "❌"
        else:
            icon = "📌"

        builder.button(
            text=f"{icon} #{app['id']} — {app['name']}",
            callback_data=f"application:{app['id']}"
        )

    builder.button(
        text="⬅️ Orqaga",
        callback_data="applications_menu"
    )

    builder.adjust(1)

    await callback.message.edit_text(
        f"<b>{title}</b>\n\n"
        "Kerakli arizani tanlang:",
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )

    await callback.answer()

# =========================================================
# ADMIN STATUS — BOG‘LANILDI
# =========================================================

@dp.callback_query(F.data.startswith("admin_contacted:"))
async def admin_contacted_handler(callback: CallbackQuery):
    await change_admin_status(
        callback=callback,
        status="contacted",
        status_text="📞 Bog‘lanildi",
        callback_prefix="admin_contacted:",
    )


# =========================================================
# ADMIN STATUS — QABUL QILINDI
# =========================================================

@dp.callback_query(F.data.startswith("admin_accepted:"))
async def admin_accepted_handler(callback: CallbackQuery):
    await change_admin_status(
        callback=callback,
        status="accepted",
        status_text="✅ Qabul qilindi",
        callback_prefix="admin_accepted:",
    )


# =========================================================
# ADMIN STATUS — RAD ETILDI
# =========================================================

@dp.callback_query(F.data.startswith("admin_rejected:"))
async def admin_rejected_handler(callback: CallbackQuery):
    await change_admin_status(
        callback=callback,
        status="rejected",
        status_text="❌ Rad etildi",
        callback_prefix="admin_rejected:",
    )
# =========================================================
# ADMIN — ARIZALAR MENYUSI
# =========================================================

@dp.message(F.text == "/applications")
async def applications_handler(message: Message):

    if message.from_user.id != ADMIN_ID:
        return

    builder = InlineKeyboardBuilder()

    builder.button(
        text="📊 Statistika",
        callback_data="statistics"
    )

    builder.button(
        text="👨‍🎓 O‘quvchilar bazasi",
        callback_data="students"
    )

    builder.button(
        text="📋 Barcha arizalar",
        callback_data="filter:all"
    )

    builder.button(
        text="🆕 Yangi arizalar",
        callback_data="filter:new"
    )

    builder.button(
        text="📞 Bog‘lanilgan",
        callback_data="filter:contacted"
    )

    builder.button(
        text="✅ Qabul qilingan",
        callback_data="filter:accepted"
    )

    builder.button(
        text="❌ Rad etilgan",
        callback_data="filter:rejected"
    )

    builder.adjust(1)

    await message.answer(
        "📋 <b>ADMIN PANEL</b>\n\n"
        "Kerakli bo‘limni tanlang:",
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )


# =========================================================
# ADMIN — ARIZALAR MENYUSI
# =========================================================

@dp.message(F.text == "/applications")
async def applications_handler(message: Message):

    if message.from_user.id != ADMIN_ID:
        return

    builder = InlineKeyboardBuilder()

    builder.button(
        text="📊 Statistika",
        callback_data="statistics"
    )

    builder.button(
        text="👨‍🎓 O‘quvchilar bazasi",
        callback_data="students"
    )

    builder.button(
        text="📋 Barcha arizalar",
        callback_data="filter:all"
    )

    builder.button(
        text="🆕 Yangi arizalar",
        callback_data="filter:new"
    )

    builder.button(
        text="📞 Bog‘lanilgan",
        callback_data="filter:contacted"
    )

    builder.button(
        text="✅ Qabul qilingan",
        callback_data="filter:accepted"
    )

    builder.button(
        text="❌ Rad etilgan",
        callback_data="filter:rejected"
    )

    builder.adjust(1)

    await message.answer(
        "📋 <b>ADMIN PANEL</b>\n\n"
        "Kerakli bo‘limni tanlang:",
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )
# =========================================================
# ADMIN — BIRTA ARIZANI KO‘RISH
# =========================================================

@dp.callback_query(
    F.data.startswith("application:")
)
async def application_detail_handler(
        callback: CallbackQuery
):

    # Faqat admin
    if callback.from_user.id != ADMIN_ID:
        await callback.answer(
            "❌ Sizda ruxsat yo‘q.",
            show_alert=True
        )
        return

    application_id = callback.data.split(":")[1]

    applications = await get_applications()

    application = None

    for app in applications:
        if str(app["id"]) == application_id:
            application = app
            break

    if application is None:
        await callback.answer(
            "❌ Ariza topilmadi.",
            show_alert=True
        )
        return

    status = application["status"]

    if status == "new":
        status_text = "🆕 Yangi"
    elif status == "contacted":
        status_text = "📞 Bog‘lanildi"
    elif status == "accepted":
        status_text = "✅ Qabul qilindi"
    elif status == "rejected":
        status_text = "❌ Rad etildi"
    else:
        status_text = status

    subject_names = {
        "russian": "🇷🇺 Rus tili",
        "english": "🇬🇧 Ingliz tili",
        "math": "🧮 Matematika",
        "mental": "🧠 Mental arifmetika"
    }

    level_names = {
        "beginner": "🌱 Boshlang‘ich",
        "middle": "📚 O‘rta",
        "advanced": "🎓 Yuqori"
    }

    subject = subject_names.get(
        application["subject"],
        application["subject"]
    )

    level = level_names.get(
        application["level"],
        application["level"]
    )

    education_format = application["education_format"]

    if not education_format:
        education_format = "🏫 Offline"

    text = (
        f"📋 <b>ARIZA #{application['id']}</b>\n\n"

        f"👤 <b>Ism:</b> {application['name']}\n"
        f"📱 <b>Telefon:</b> {application['phone']}\n"
        f"🎂 <b>Yosh:</b> {application['age']}\n"
        f"📍 <b>Manzil:</b> {application['location']}\n\n"

        f"📚 <b>Fan:</b> {subject}\n"
        f"📊 <b>Daraja:</b> {level}\n"
        f"💻 <b>Format:</b> {education_format}\n"
        f"🕐 <b>Dars vaqti:</b> "
        f"{TIMES['uz'].get(application['lesson_time'], application['lesson_time'])}\n"
        f"💰 <b>Narx:</b> "
        f"{application['price']:,} so‘m\n\n"

        f"📌 <b>Status:</b> {status_text}\n"
        f"📅 <b>Sana:</b> {application['created_at']}"
    )

    builder = InlineKeyboardBuilder()

    # Status tugmalari
    if status != "contacted":
        builder.button(
            text="📞 Bog‘lanildi",
            callback_data=f"admin_contacted:{application_id}"
        )

    if status != "accepted":
        builder.button(
            text="✅ Qabul qilindi",
            callback_data=f"admin_accepted:{application_id}"
        )

    if status != "rejected":
        builder.button(
            text="❌ Rad etildi",
            callback_data=f"admin_rejected:{application_id}"
        )

    # Orqaga
    builder.button(
        text="⬅️ Orqaga",
        callback_data="applications_back"
    )

    builder.adjust(1)

    await callback.message.edit_text(
        text,
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )

    await callback.answer()



# =========================================================
# ADMIN — ARIZALAR RO‘YXATIGA QAYTISH
# =========================================================

@dp.callback_query(
    F.data == "applications_back"
)
async def applications_back_handler(
        callback: CallbackQuery
):

    if callback.from_user.id != ADMIN_ID:
        await callback.answer(
            "❌ Sizda ruxsat yo‘q.",
            show_alert=True
        )
        return

    applications = await get_applications()

    if not applications:
        await callback.message.edit_text(
            "📋 Hozircha arizalar mavjud emas."
        )
        await callback.answer()
        return

    builder = InlineKeyboardBuilder()

    for app in applications:

        status = app["status"]

        if status == "new":
            status_icon = "🆕"
        elif status == "contacted":
            status_icon = "📞"
        elif status == "accepted":
            status_icon = "✅"
        elif status == "rejected":
            status_icon = "❌"
        else:
            status_icon = "📌"

        builder.button(
            text=f"{status_icon} #{app['id']} — {app['name']}",
            callback_data=f"application:{app['id']}"
        )

    builder.adjust(1)

    await callback.message.edit_text(
        "📋 <b>BARCHA ARIZALAR</b>\n\n"
        "Kerakli arizani tanlang:",
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )

    await callback.answer()


# =========================================================
# ADMIN — FILTER MENYUSIGA QAYTISH
# =========================================================

@dp.callback_query(
    F.data == "applications_menu"
)
async def applications_menu_handler(
        callback: CallbackQuery
):

    if callback.from_user.id != ADMIN_ID:
        await callback.answer(
            "❌ Sizda ruxsat yo‘q.",
            show_alert=True
        )
        return

    builder = InlineKeyboardBuilder()

    builder.button(
        text="📊 Statistika",
        callback_data="statistics"
    )

    builder.button(
        text="👨‍🎓 O‘quvchilar bazasi",
        callback_data="students"
    )

    builder.button(
        text="🆕 Yangi arizalar",
        callback_data="filter:new"
    )

    builder.button(
        text="📞 Bog‘lanilgan",
        callback_data="filter:contacted"
    )

    builder.button(
        text="✅ Qabul qilingan",
        callback_data="filter:accepted"
    )

    builder.button(
        text="❌ Rad etilgan",
        callback_data="filter:rejected"
    )

    builder.button(
        text="📋 Barcha arizalar",
        callback_data="filter:all"
    )

    builder.adjust(1)

    await callback.message.edit_text(
        "📋 <b>ARIZALAR BO‘LIMI</b>\n\n"
        "Qaysi arizalarni ko‘rmoqchisiz?",
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )

    await callback.answer()

# =========================================================
# BOTNI ISHGA TUSHIRISH
# =========================================================

async def main():
    print("Bot ishga tushdi...")
    await create_database()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
