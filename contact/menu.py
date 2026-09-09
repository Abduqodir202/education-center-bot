from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()


@router.callback_query(F.data == "contact")
async def contact_handler(callback: CallbackQuery):

    builder = InlineKeyboardBuilder()

    builder.button(
        text="📞 +998 77 182 47 47",
        url="https://wa.me/998771824747"
    )

    builder.button(
        text="📍 Bizning manzil",
        url="https://www.google.com/maps?q=40.902583,69.643833"
    )

    builder.adjust(1)

    await callback.message.edit_text(
        "📞 <b>Biz bilan bog‘lanish</b>\n\n"
        "📱 Telefon: <b>+998 77 182 47 47</b>\n\n"
        "📍 <b>Manzil:</b>\n"
        "Ohangaron shahri, Anhor binosi, 2-qavat",
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )

    await callback.answer()