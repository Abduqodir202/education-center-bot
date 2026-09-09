from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()


# =========================================================
# 📚 KURSLARIMIZ
# =========================================================
@router.callback_query(F.data == "courses")
async def courses_handler(callback: CallbackQuery):
    builder = InlineKeyboardBuilder()

    builder.button(
        text="🇷🇺 Rus tili",
        callback_data="course_russian"
    )

    builder.button(
        text="🧮 Matematika",
        callback_data="course_math"
    )

    builder.button(
        text="🇬🇧 Ingliz tili",
        callback_data="course_english"
    )

    builder.button(
        text="⬅️ Orqaga",
        callback_data="back_main"
    )

    builder.adjust(1)

    await callback.message.edit_text(
        "📚 <b>KURSLARIMIZ</b>\n\n"
        "🎓 ZAMON O‘QUV MARKAZIDA quyidagi yo‘nalishlar "
        "bo‘yicha ta’lim olishingiz mumkin:\n\n"
        "👇 O‘zingizga kerakli kursni tanlang:",
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )

    await callback.answer()


# =========================================================
# 🇷🇺 RUS TILI
# =========================================================
@router.callback_query(F.data == "course_russian")
async def russian_course_handler(callback: CallbackQuery):

    text = (
        "🇷🇺 <b>RUS TILI KURSI</b>\n\n"

        "📖 <b>Kurs haqida:</b>\n"
        "Rus tilini boshlang‘ich darajadan yuqori darajagacha "
        "bosqichma-bosqich o‘rganish.\n\n"

        "🎯 <b>Kurs maqsadi:</b>\n"
        "✅ Grammatikani mustahkamlash\n"
        "✅ So‘z boyligini oshirish\n"
        "✅ To‘g‘ri talaffuzni rivojlantirish\n"
        "✅ Og‘zaki va yozma nutqni yaxshilash\n"
        "✅ Milliy va xalqaro sertifikatlarga tayyorlanish\n\n"

        "⭐ <b>KURSNING AFZALLIKLARI:</b>\n"
        "📚 Har oy maxsus nazorat imtihonlari\n"
        "📝 DTM formatidagi sinov testlari\n"
        "🔄 O‘tilgan mavzularni muntazam takrorlash\n"
        "🧠 O‘rganilgan bilimlarni mustahkamlash\n"
        "📊 O‘quvchi natijalarini muntazam nazorat qilish\n"
        "🏆 Olimpiada va tanlovlarga tayyorgarlik\n\n"

        "👨‍🏫 Professional ustozlar\n"
        "🏫 Offline ta’lim\n"
        "💻 Online ta’lim\n"
        "⏳ Kurs davomiyligi: 3 oydan 1 yilgacha"
    )

    builder = InlineKeyboardBuilder()

    builder.button(
        text="💰 Kurs narxi",
        callback_data="price_russian"
    )

    builder.button(
        text="📝 Ariza berish",
        callback_data="apply"
    )

    builder.button(
        text="⬅️ Kurslarga qaytish",
        callback_data="courses"
    )

    builder.adjust(1)

    await callback.message.edit_text(
        text,
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )

    await callback.answer()


# =========================================================
# 🧮 MATEMATIKA
# =========================================================
@router.callback_query(F.data == "course_math")
async def math_course_handler(callback: CallbackQuery):

    text = (
        "🧮 <b>MATEMATIKA KURSI</b>\n\n"

        "📖 <b>Kurs haqida:</b>\n"
        "Matematika fanini tushunarli va amaliy usulda "
        "o‘rganishga mo‘ljallangan maxsus dastur.\n\n"

        "🎯 <b>Kurs maqsadi:</b>\n"
        "✅ Matematik fikrlashni rivojlantirish\n"
        "✅ Masalalarni tez va to‘g‘ri yechishni o‘rganish\n"
        "✅ Maktab dasturini mustahkamlash\n"
        "✅ Nazorat va imtihonlarga tayyorlanish\n"
        "✅ DTM testlariga tayyorlanish\n\n"

        "⭐ <b>KURSNING AFZALLIKLARI:</b>\n"
        "📚 Har oy maxsus nazorat imtihonlari\n"
        "📝 DTM formatidagi sinov testlari\n"
        "🔄 O‘tilgan mavzularni muntazam takrorlash\n"
        "🧠 O‘rganilgan bilimlarni mustahkamlash\n"
        "📊 O‘quvchi natijalarini muntazam nazorat qilish\n"
        "🏆 Olimpiada va tanlovlarga tayyorgarlik\n\n"

        "👨‍🏫 Tajribali ustozlar\n"
        "🏫 Offline ta’lim\n"
        "⏳ Kurs davomiyligi: 3 oydan 1 yilgacha"
    )

    builder = InlineKeyboardBuilder()

    builder.button(
        text="💰 Kurs narxi",
        callback_data="price_math"
    )

    builder.button(
        text="📝 Ariza berish",
        callback_data="apply"
    )

    builder.button(
        text="⬅️ Kurslarga qaytish",
        callback_data="courses"
    )

    builder.adjust(1)

    await callback.message.edit_text(
        text,
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )

    await callback.answer()


# =========================================================
# 🇬🇧 INGLIZ TILI
# =========================================================
@router.callback_query(F.data == "course_english")
async def english_course_handler(callback: CallbackQuery):

    text = (
        "🇬🇧 <b>INGLIZ TILI KURSI</b>\n\n"

        "📖 <b>Kurs haqida:</b>\n"
        "Ingliz tilini bosqichma-bosqich o‘rganish va "
        "muloqot ko‘nikmalarini rivojlantirish.\n\n"

        "🎯 <b>Kurs maqsadi:</b>\n"
        "✅ Grammar\n"
        "✅ Speaking\n"
        "✅ Listening\n"
        "✅ Reading\n"
        "✅ Writing\n"
        "✅ Lug‘at boyligini oshirish\n"
        "✅ Imtihon va sertifikatlarga tayyorlanish\n\n"

        "⭐ <b>KURSNING AFZALLIKLARI:</b>\n"
        "📚 Har oy maxsus nazorat imtihonlari\n"
        "📝 Maxsus sinov testlari\n"
        "🔄 O‘tilgan mavzularni muntazam takrorlash\n"
        "🧠 O‘rganilgan bilimlarni mustahkamlash\n"
        "📊 O‘quvchi natijalarini muntazam nazorat qilish\n"
        "🏆 Olimpiada va tanlovlarga tayyorgarlik\n\n"

        "👨‍🏫 Professional ustozlar\n"
        "🏫 Offline ta’lim\n"
        "⏳ Kurs davomiyligi: 3 oydan 1 yilgacha"
    )

    builder = InlineKeyboardBuilder()

    builder.button(
        text="💰 Kurs narxi",
        callback_data="price_english"
    )

    builder.button(
        text="📝 Ariza berish",
        callback_data="apply"
    )

    builder.button(
        text="⬅️ Kurslarga qaytish",
        callback_data="courses"
    )

    builder.adjust(1)

    await callback.message.edit_text(
        text,
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )

    await callback.answer()