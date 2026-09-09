from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()


@router.callback_query(F.data == "about")
async def about_handler(callback: CallbackQuery):
    text = (
        "🏢 <b>ZAMON O‘QUV MARKAZI</b>\n\n"

        "📅 <b>2022-yildan beri</b> sifatli ta’lim xizmatlarini "
        "taqdim etib kelayotgan Zamon o‘quv markazi "
        "o‘quvchilarning bilim va kelajakdagi maqsadlariga "
        "erishishiga yordam beradi.\n\n"

        "🎓 <b>ASOSIY YO‘NALISHLARIMIZ</b>\n\n"

        "🏛 <b>Oliy ta’limga professional tayyorgarlik</b>\n"
        "Abituriyentlarni oliy ta’lim muassasalariga kirish "
        "imtihonlariga tizimli va professional tayyorlaymiz.\n\n"

        "📜 <b>Milliy sertifikat</b>\n"
        "Fanlar bo‘yicha milliy sertifikat imtihonlariga "
        "puxta tayyorgarlik ko‘rishga yordam beramiz.\n\n"

        "🌎 <b>Xalqaro sertifikatlar</b>\n"
        "Xalqaro darajadagi sertifikat imtihonlariga "
        "tayyorgarlik yo‘nalishlarini taklif qilamiz.\n\n"

        "👨‍🏫 <b>Professional ustozlar</b>\n"
        "Tajribali va o‘z fanini yaxshi biladigan ustozlar "
        "bilan sifatli ta’lim jarayonini tashkil qilamiz.\n\n"

        "🎯 <b>BIZNING MAQSADIMIZ</b>\n"
        "Har bir o‘quvchining imkoniyatini ochish, "
        "yuqori natijalarga erishish va kelajakdagi "
        "ta’lim yo‘lida ishonchli poydevor yaratish.\n\n"

        "🚀 <b>ZAMON — bilim, natija va kelajak sari!</b>"
    )

    builder = InlineKeyboardBuilder()

    builder.button(
        text="⬅️ Orqaga",
        callback_data="back_main"
    )

    await callback.message.edit_text(
        text,
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )

    await callback.answer()