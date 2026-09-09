from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()


# =========================================================
# 💰 KURS NARXLARI — FANLAR
# =========================================================
@router.callback_query(F.data == "prices")
async def prices_handler(callback: CallbackQuery):
    builder = InlineKeyboardBuilder()

    builder.button(
        text="🇷🇺 Rus tili",
        callback_data="price_russian"
    )

    builder.button(
        text="🧮 Matematika",
        callback_data="price_math"
    )

    builder.button(
        text="🇬🇧 Ingliz tili",
        callback_data="price_english"
    )

    builder.button(
        text="⬅️ Orqaga",
        callback_data="back_main"
    )

    builder.adjust(1)

    await callback.message.edit_text(
        "💰 <b>KURS NARXLARI</b>\n\n"
        "🎓 O‘zingizga kerakli fanni tanlang:",
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )

    await callback.answer()


# =========================================================
# 🇷🇺 RUS TILI
# =========================================================
@router.callback_query(F.data == "price_russian")
async def russian_price_handler(callback: CallbackQuery):

    text = (
        "🇷🇺 <b>RUS TILI</b>\n\n"

        "🏫 <b>OFFLINE TA’LIM</b>\n\n"

        "👦 <b>12 yoshgacha:</b>\n"
        "💰 300 000 so‘m / oy\n\n"

        "👦 <b>12–15 yosh:</b>\n"
        "💰 400 000 so‘m / oy\n\n"

        "👨 <b>16–30 yosh:</b>\n"
        "💰 500 000 so‘m / oy\n\n"

        "👨‍💼 <b>30 yoshdan yuqori:</b>\n"
        "💰 600 000 so‘m / oy\n\n"

        "💻 <b>ONLINE TA’LIM</b>\n"
        "💰 200 000 so‘m / oy\n\n"

        "⏳ <b>Kurs davomiyligi:</b>\n"
        "📅 3 oydan 1 yilgacha\n\n"

    )

    builder = InlineKeyboardBuilder()

    builder.button(
        text="📝 Ariza berish",
        callback_data="apply"
    )

    builder.button(
        text="⬅️ Kurslarga qaytish",
        callback_data="prices"
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
@router.callback_query(F.data == "price_math")
async def math_price_handler(callback: CallbackQuery):

    text = (
        "🧮 <b>MATEMATIKA</b>\n\n"

        "🏫 <b>OFFLINE TA’LIM</b>\n\n"

        "👦 <b>16 yoshgacha:</b>\n"
        "💰 400 000 so‘m / oy\n\n"

        "👨 <b>16 yoshdan yuqori:</b>\n"
        "💰 500 000 so‘m / oy\n\n"

        "⏳ <b>Kurs davomiyligi:</b>\n"
        "📅 3 oydan 1 yilgacha\n\n"
    )

    builder = InlineKeyboardBuilder()

    builder.button(
        text="📝 Ariza berish",
        callback_data="apply"
    )

    builder.button(
        text="⬅️ Kurslarga qaytish",
        callback_data="prices"
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
@router.callback_query(F.data == "price_english")
async def english_price_handler(callback: CallbackQuery):

    text = (
        "🇬🇧 <b>INGLIZ TILI</b>\n\n"

        "🏫 <b>OFFLINE TA’LIM</b>\n\n"

        "👦 <b>16 yoshgacha:</b>\n"
        "💰 400 000 so‘m / oy\n\n"

        "👨 <b>16 yoshdan yuqori:</b>\n"
        "💰 500 000 so‘m / oy\n\n"

        "⏳ <b>Kurs davomiyligi:</b>\n"
        "📅 3 oydan 1 yilgacha\n\n"

    )

    builder = InlineKeyboardBuilder()

    builder.button(
        text="📝 Ariza berish",
        callback_data="apply"
    )

    builder.button(
        text="⬅️ Kurslarga qaytish",
        callback_data="prices"
    )

    builder.adjust(1)

    await callback.message.edit_text(
        text,
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )

    await callback.answer()