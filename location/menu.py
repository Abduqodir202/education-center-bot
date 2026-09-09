from aiogram import Router, F
from aiogram.types import CallbackQuery
# from aiogram.types import Location
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()


# =========================================================
# 📍 BIZNING MANZIL
# =========================================================
@router.callback_query(F.data == "location")
async def location_handler(callback: CallbackQuery):

    # 📍 ANIQ KOORDINATALARNI KEYIN KIRITAMIZ
    latitude = 40.902583
    longitude = 69.643833

    await callback.message.answer_location(
        latitude=latitude,
        longitude=longitude
    )

    builder = InlineKeyboardBuilder()

    builder.button(
        text="📝 Ariza berish",
        callback_data="apply"
    )

    builder.button(
        text="⬅️ Asosiy menyu",
        callback_data="back_main"
    )

    builder.adjust(1)

    await callback.message.answer(
        "📍 <b>BIZNING MANZIL</b>\n\n"
        "🏢 <b>ZAMON O‘QUV MARKAZI</b>\n\n"
        "📍 Ohangaron shahri\n"
        "🏢 Anhor binosi\n"
        "🏢 2-qavat\n\n"
        "📌 <b>Manzil:</b>\n"
        "Ohangaron shahri, Anhor binosi, 2-qavat",
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )

    await callback.answer()