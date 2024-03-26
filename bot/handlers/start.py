from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __
from aiogram.utils.markdown import hbold
from sqlalchemy import select, insert
from sqlalchemy.sql.operators import ilike_op

from bot.buttons.inline import our_network_btn
from bot.buttons.reply import main_menu_btn
from bot.dispatcher import dp
from db.models import User, session, Book, Contact

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    query = select(User).where(User.chat_id == message.from_user.id)
    user = session.execute(query).fetchone()
    if not user:
        user = {
            "chat_id": message.from_user.id,
            "username": message.from_user.username,
            "fullname": message.from_user.full_name
        }
        query = insert(User).values(**user)
        session.execute(query)
        session.commit()

    await message.answer(_("Hello ") + f"{hbold(message.from_user.full_name)}!", parse_mode=ParseMode.HTML,
                         reply_markup=main_menu_btn())


@router.message(F.text == __("🔵 Our Network"))
async def our_network_handler(msg: Message):
    await msg.answer(text=_("🔵 Our Network"), reply_markup=our_network_btn())


@router.message(F.text == __("📞 Contact us"))
async def our_network_handler(msg: Message):
    contact: Contact = session.execute(select(Contact)).scalar()
    text = f"""
    Telegram: {contact.bot_link}

📞 {contact.phone_number}

🤖 Bot P20 guruhi (@Dilshod_Absaitov) tomonidan tayyorlandi.
    """
    await msg.answer(text=text)

@router.inline_query()
async def show_product(inline_query: InlineQuery):
    books: list[Book] = session.execute(select(Book).filter(ilike_op(Book.title, f"%{inline_query.query}%"))).scalars()
    result = [
        InlineQueryResultArticle(
            id=str(book.id),
            title=book.title,
            description=str(f"P20 books\n💴 Narxi: {book.price} so'm"),
            thumbnail_url=book.photo,
            input_message_content=InputTextMessageContent(message_text=book.title)
        )
        for book in books]
    await inline_query.answer(result, cache_time=5, is_personal=True)
