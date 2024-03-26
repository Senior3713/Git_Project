from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.i18n import gettext as _


def main_menu_btn():
    rkm = ReplyKeyboardBuilder()
    rkm.add(*[
        KeyboardButton(text=_("📚 books")),
        KeyboardButton(text=_("📄 My Orders")),
        KeyboardButton(text=_("🔵 Our Network")),
        KeyboardButton(text=_("📞 Contact us"))
    ])
    rkm.adjust(1, 1, 2)
    return rkm.as_markup(resize_keyboard=True)


def lang_btn():
    rkm = ReplyKeyboardBuilder()
    rkm.add(*[
        KeyboardButton(text=_("🇺🇿 uzbek")),
        KeyboardButton(text=_("🇬🇧 english"))
    ])
    return rkm.as_markup(resize_keyboard=True)
