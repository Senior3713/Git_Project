from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import select
from aiogram.utils.i18n import gettext as _


from db.models import Network, session, Category, Book


def our_network_btn():
    ikm = InlineKeyboardBuilder()
    networks:list[Network] = session.execute(select(Network)).scalars()
    ikm.add(*[InlineKeyboardButton(text=network.title , url=network.link) for network in networks])
    ikm.adjust(1, repeat=True)
    return ikm.as_markup()

def category_list_btn():
    ikm = InlineKeyboardBuilder()
    categories: list[Category] = session.execute(select(Category)).scalars()
    ikm.add(*[InlineKeyboardButton(text=category.name , callback_data=f"category_{category.name}_{category.id}") for category in categories])
    ikm.add(*[InlineKeyboardButton(text = _("🔎 Search") ,  switch_inline_query_current_chat='')])
    ikm.adjust(2 , repeat=True)
    return ikm.as_markup()

def book_list_btn(category_id):
    ikm = InlineKeyboardBuilder()
    books:list[Book] = session.execute(select(Book).where(Book.category_id == category_id)).scalars()
    ikm.add(*[InlineKeyboardButton(text=book.title , callback_data=f"book_{book.id}") for book in books])
    ikm.add(*[InlineKeyboardButton(text = _("◀️Back") ,  callback_data='book_back')])
    ikm.adjust(2 , repeat=True)
    return ikm.as_markup()


def order_btn(count = 1):
    ikm = InlineKeyboardBuilder()
    ikm.add(*[
        InlineKeyboardButton(text="➖", callback_data=f'order_count_minus_{count}'),
        InlineKeyboardButton(text=str(count), callback_data='count'),
        InlineKeyboardButton(text=_("➕"), callback_data=f'order_count_plus_{count}'),
        InlineKeyboardButton(text=_("◀️Back"), callback_data='order_back'),
        InlineKeyboardButton(text=_("🛒 Add to cart"), callback_data='order_add')
    ])
    ikm.adjust(3,2)
    return ikm.as_markup()



