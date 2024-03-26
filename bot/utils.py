from aiogram.utils.i18n import gettext as _
from sqlalchemy import select

from db.models import Book, session


def book_make_detail(book_id):
    book: Book = session.execute(select(Book).where(Book.id == book_id)).scalar()
    caption = """
    {title}: {book_title}
{author}: {book_author}
{genre}: {book_category_name} 
{page}: {book_page}
{vol}: {book_vol_name}
{about}: {book_description}
{price}: {book_price} {book_money_type_value}
    """.format(
        title=_("🔹 Title"),
        book_title=book.title,
        author=_("✍🏻Author"),
        book_author=book.author,
        genre=_("🟤 Genre"),
        book_category_name=book.category.name,
        page=_("📑 Page"),
        book_page = book.page,
        vol = _("📕 Vol") ,
        book_vol_name = book.vol.name,
        about = _("📖 About"),
        book_description = book.description,
        price = _("💸 Price"),
        book_price = book.price,
        book_money_type_value = book.money_type.value
        )
    photo = book.photo
    return caption, photo
