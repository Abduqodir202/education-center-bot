from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()


@router.callback_query(F.data == 'results')
async def results_handler(callback: CallbackQuery):
    text = (

        "🏆 <b>BIZNING NATIJALAR</b>\n\n"

        "🥇 <b>1-NATIJA</b>\n\n"

        "👩‍🎓 <b>Aliyeva Shabnam</b>\n\n"

        "🇰🇬 Qirg‘iziston Respublikasida "
        "rus tili fanidan o‘tkazilgan "
        "<b>Xalqaro Olimpiada</b>da\n\n"

        "🥇 <b>faxrli 1-o‘rinni egalladi!</b>\n\n"

        "🎁 Natijada Shabnam\n"
        "🇯🇵 <b>Yaponiyaga 100% vaucher</b> "
        "sohibasi bo‘ldi! 🇯🇵\n\n"

        "👏 <b>Shabnamni ushbu katta yutug‘i bilan "
        "tabriklaymiz!</b>\n\n"

        "🎓 Zamon o‘quv markazi — "
        "o‘quvchilarining yutuqlari bilan faxrlanadi! ❤️\n\n"

        "🚀 <b>Keyingi katta natija — sizniki bo‘lishi mumkin!</b>"
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
        parse_mode='HTML'
    )

    await callback.answer()