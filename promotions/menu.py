from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder


router = Router()


# =========================================================
# 🎁 AKSIYALAR VA IMTIYOZLAR
# =========================================================

@router.callback_query(F.data == "promotions")
async def promotions_handler(callback: CallbackQuery):

    text = (
        "🎁 <b>AKSIYALAR VA IMTIYOZLAR</b>\n\n"

        "🔥 <b>ZAMON O‘QUV MARKAZIDA MAXSUS IMKONIYATLAR!</b>\n\n"

        "📚 <b>2 TA FANGA QATNASHING — 50 000 SO‘M CHEGIRMA!</b>\n"
        "Agar o‘quvchi bir vaqtning o‘zida "
        "2 ta fan bo‘yicha ta’lim olsa "
        "(masalan: 🇷🇺 Rus tili + 🧮 Matematika), "
        "<b>50 000 so‘m chegirma</b> taqdim etiladi.\n\n"

        "❤️ <b>MAXSUS IJTIMOIY IMTIYOZ</b>\n"
        "Boquvchisini yo‘qotgan "
        "<b>16 yoshgacha bo‘lgan bolalar</b> "
        "uchun maxsus imtiyozlar mavjud.\n\n"

        "👨‍👩‍👧‍👦 <b>OILAVIY CHEGIRMA — 100 000 SO‘M!</b>\n"
        "Agar bir oiladan <b>2 nafar o‘quvchi</b> "
        "bizning markazimizda ta’lim olsa, "
        "<b>100 000 so‘m chegirma</b> beriladi.\n\n"

        "👥 <b>DO‘STINGIZNI OLIB KELING — 10% CHEGIRMA!</b>\n"
        "O‘zingiz bilan yangi o‘quvchi olib kelsangiz, "
        "sizga <b>10% chegirma</b> taqdim etiladi.\n\n"

        "🎓 <b>ZAMON O‘QUV MARKAZI</b>\n"
        "Sifatli ta’lim — hamyonbop narxlar — "
        "o‘quvchilar uchun ko‘proq imkoniyatlar! ❤️\n\n"

        "🚀 <b>Imkoniyatni qo‘ldan boy bermang!</b>"
    )

    builder = InlineKeyboardBuilder()

    builder.button(
        text="📝 Ariza berish",
        callback_data="apply"
    )

    builder.button(
        text="⬅️ Orqaga",
        callback_data="back_main"
    )

    builder.adjust(1)

    await callback.message.edit_text(
        text,
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )

    await callback.answer()