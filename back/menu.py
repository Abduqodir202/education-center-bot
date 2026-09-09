from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()


@router.callback_query(F.data == "back_main")
async def back_main_handler(callback: CallbackQuery):

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
        text="💬 O‘quvchilar fikri",
        callback_data="reviews"
    )

    builder.button(
        text="🎁 Aksiyalar va imtiyozlar",
        callback_data="promotions"
    )

    builder.button(
        text="📅 Dars jadvali",
        callback_data="schedule"
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

    await callback.message.edit_text(
        "🎓 <b>ZAMON O‘QUV MARKAZI</b>\n\n"
        "Assalomu alaykum! 👋\n\n"
        "Quyidagi bo‘limlardan birini tanlang:",
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )

    await callback.answer()