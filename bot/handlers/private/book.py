from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __

from bot.buttons.inline import category_list_btn, book_list_btn, order_btn
from bot.utils import book_make_detail

book_router = Router()

@book_router.message(F.text == __("📚 books"))
async def book_handler(msg : Message):
    await msg.answer(text = _("Choose one of the categories"), reply_markup=category_list_btn())

@book_router.callback_query(F.data.startswith("category_"))
async def category_handler(call : CallbackQuery, state : FSMContext ):
    category_id = int(call.data.split("_")[2])
    category_name = call.data.split("_")[1]
    await state.update_data({"category_id" : category_id})
    await call.message.edit_text(text = category_name , reply_markup=book_list_btn(category_id))

@book_router.callback_query(F.data == "book_back")
async def book_back_handler(call : CallbackQuery , state = FSMContext):
    await call.message.edit_text(text = _("Choose one of the categories"), reply_markup=category_list_btn())


@book_router.callback_query(F.data.startswith("book_"))
async def book_detail_handler(call : CallbackQuery , state : FSMContext):
    await call.message.delete()
    book_id = int(call.data.split('_')[1])
    caption , photo = book_make_detail(book_id)
    await state.update_data({"count": 1 , "book_id" : book_id})
    await call.message.answer_photo(photo=photo , caption=caption , reply_markup=order_btn())


@book_router.callback_query(F.data.startswith("order_count_minus_"))
async def minus_count_handler(call : CallbackQuery , state : FSMContext):
    count = int(call.data.split("_")[-1])
    if count != 1:
        count = count - 1
        await state.update_data({"count" : count})
        await call.message.edit_reply_markup(reply_markup=order_btn(count))
    else:
        await call.answer(text = _("You can order at least one book 😊") , show_alert=True)


@book_router.callback_query(F.data.startswith("order_count_plus_"))
async def plus_count_handler(call : CallbackQuery , state : FSMContext):
    count = int(call.data.split("_")[-1])
    count = count + 1
    await state.update_data({"count" : count})
    await call.message.edit_reply_markup(reply_markup=order_btn(count))


@book_router.callback_query(F.data == "order_back")
async def order_back_handler(call : CallbackQuery , state : FSMContext):
    await call.message.delete()
    await call.message.answer(text = _("Choose one of the categories"), reply_markup=category_list_btn())












