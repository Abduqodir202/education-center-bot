from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()


# =========================================================
# 👨‍🏫 BIZNING USTOZLAR
# =========================================================
@router.callback_query(F.data == "teachers")
async def teachers_handler(callback: CallbackQuery):

    builder = InlineKeyboardBuilder()

    builder.button(
        text="👩‍🏫 Rus tili o‘qituvchisi",
        callback_data="teacher_russian"
    )

    builder.button(
        text="👨‍🏫 Matematika o‘qituvchisi",
        callback_data="teacher_math"
    )

    builder.button(
        text="👩‍🏫 Ingliz tili o‘qituvchisi",
        callback_data="teacher_english"
    )

    builder.button(
        text="⬅️ Orqaga",
        callback_data="back_main"
    )

    builder.adjust(1)

    await callback.message.edit_text(
        "👨‍🏫 <b>BIZNING USTOZLAR</b>\n\n"
        "🎓 ZAMON O‘QUV MARKAZI ustozlari — "
        "o‘z fanlari bo‘yicha tajribali va malakali mutaxassislar.\n\n"
        "📚 Har bir o‘quvchiga individual yondashuv\n"
        "📊 Natijalarni muntazam nazorat qilish\n"
        "🎯 Imtihon va olimpiadalarga tayyorlash\n\n"
        "👇 Ustozni tanlang:",
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )

    await callback.answer()


# =========================================================
# 🇷🇺 RUS TILI USTOZI
# =========================================================
@router.callback_query(F.data == "teacher_russian")
async def russian_teacher_handler(callback: CallbackQuery):
    text = (
        "🇷🇺 <b>RUS TILI KURSI</b>\n\n"

        "👩‍🏫 <b>Rus tili ustozi:</b>\n"
        "Madina Axmedova\n\n"

        "🎓 <b>Oliy ma'lumotli mutaxassis.</b>\n\n"

        "⏳ <b>20 yildan ortiq pedagogik tajriba.</b>\n\n"

        "👨‍🎓 <b>1000+ nafar shogirdlar tayyorlagan.</b>\n\n"

        "🏆 <b>100+ nafar o‘quvchilari</b>\n"
        "Milliy va Xalqaro sertifikatlarni qo‘lga kiritgan.\n\n"

        "📚 <b>Kurs davomida:</b>\n"
        "• Grammatikani mukammal o‘rganasiz.\n"
        "• Erkin gapirishni boshlaysiz.\n"
        "• Milliy sertifikatga tayyorlanasiz.\n"
        "• Xalqaro sertifikatlarga tayyorlanasiz.\n\n"

        "⭐ <b>Kursning afzalliklari:</b>\n"
        "📚 Har oy maxsus nazorat imtihonlari\n"
        "📝 DTM formatidagi sinov testlari\n"
        "🔄 O‘tilgan mavzularni muntazam takrorlash\n"
        "🧠 O‘rganilgan bilimlarni mustahkamlash\n"
        "📊 O‘quvchi natijalarini nazorat qilish\n\n"

        "💻 <b>Ta'lim shakli:</b>\n"
        "Online va Offline.\n\n"

        "🎯 Boshlang‘ich, O‘rta va Yuqori darajalar mavjud."
    )
    builder = InlineKeyboardBuilder()

    builder.button(
        text="📝 Ariza berish",
        callback_data="apply"
    )

    builder.button(
        text="⬅️ Ustozlarga qaytish",
        callback_data="teachers"
    )

    builder.adjust(1)

    await callback.message.edit_text(
        text,
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )

    await callback.answer()


# =========================================================
# 🧮 MATEMATIKA USTOZI
# =========================================================
@router.callback_query(F.data == "teacher_math")
async def math_teacher_handler(callback: CallbackQuery):
    text = (
        "🧮 <b>MATEMATIKA KURSI</b>\n\n"

        "👨‍🏫 <b>Matematika fani ustozi:</b>\n"
        "Zikriyo Abdusamatov\n\n"

        "🏢 <b>ZAMON O‘QUV MARKAZI ASOSCHISI</b>\n\n"

        "🎓 <b>Oliy ma'lumotli mutaxassis.</b>\n\n"

        "⏳ <b>9 yillik pedagogik tajribaga ega tajribali ustoz.</b>\n\n"

        "👨‍🎓 <b>1000 dan ortiq shogirdlar</b>\n"
        "ustozdan ta'lim olib, o‘z bilimlarini mustahkamlagan "
        "va ko‘plab o‘quvchilar oliy ta'lim muassasalariga "
        "o‘qishga kirgan.\n\n"

        "🏆 <b>Asosiy maqsad:</b>\n"
        "O‘quvchilarga matematikani chuqur va tushunarli "
        "o‘rgatish hamda yuqori natijalarga erishishiga yordam berish.\n\n"

        "📚 <b>Kurs davomida:</b>\n"
        "• Mavzularni bosqichma-bosqich o‘rganasiz.\n"
        "• Murakkab masalalarni yechish usullarini o‘rganasiz.\n"
        "• Matematik fikrlash qobiliyatingiz rivojlanadi.\n"
        "• DTM formatidagi testlarga tayyorlanasiz.\n"
        "• Imtihonlarga puxta tayyorgarlik ko‘rasiz.\n"
        "• Olimpiada va tanlovlarga tayyorlanish imkoniyati mavjud.\n\n"

        "⭐ <b>KURSNING AFZALLIKLARI:</b>\n"
        "📚 Har oy maxsus nazorat imtihonlari\n"
        "📝 DTM formatidagi sinov testlari\n"
        "🔄 O‘tilgan mavzularni muntazam takrorlash\n"
        "🧠 O‘rganilgan bilimlarni mustahkamlash\n"
        "📊 O‘quvchi natijalarini muntazam nazorat qilish\n"
        "🎯 Har bir o‘quvchiga individual yondashuv\n\n"

        "💻 <b>Ta'lim shakli:</b>\n"
        "Offline.\n\n"

        "🎯 <b>Kurs yo‘nalishi:</b>\n"
        "Maktab o‘quvchilari, abituriyentlar va "
        "matematika fanini chuqur o‘rganishni istaganlar uchun."
    )
    builder = InlineKeyboardBuilder()

    builder.button(
        text="📝 Ariza berish",
        callback_data="apply"
    )

    builder.button(
        text="⬅️ Ustozlarga qaytish",
        callback_data="teachers"
    )

    builder.adjust(1)

    await callback.message.edit_text(
        text,
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )

    await callback.answer()


# =========================================================
# 🇬🇧 INGLIZ TILI USTOZI
# =========================================================
@router.callback_query(F.data == "teacher_english")
async def english_teacher_handler(callback: CallbackQuery):

    text = (
        "👩‍🏫 <b>INGLIZ TILI O‘QITUVCHISI</b>\n\n"

        "📚 <b>Yo‘nalish:</b> Ingliz tili\n"
        "🎓 <b>Ta’lim:</b> Maktab o‘quvchilari va abituriyentlar\n\n"

        "🎯 <b>Asosiy yo‘nalishlar:</b>\n"
        "• Grammar\n"
        "• Speaking\n"
        "• Listening\n"
        "• Reading\n"
        "• Writing\n"
        "• Lug‘at boyligini oshirish\n"
        "• Imtihon va sertifikatlarga tayyorgarlik\n\n"

        "⭐ <b>O‘qitish uslubi:</b>\n"
        "Zamonaviy metodlar asosida amaliy va "
        "samarali ingliz tili mashg‘ulotlari."
    )

    builder = InlineKeyboardBuilder()

    builder.button(
        text="📝 Ariza berish",
        callback_data="apply"
    )

    builder.button(
        text="⬅️ Ustozlarga qaytish",
        callback_data="teachers"
    )

    builder.adjust(1)

    await callback.message.edit_text(
        text,
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )

    await callback.answer()