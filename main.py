import asyncio
import logging
import sys
from aiogram import Bot
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from bot.handlers import *
from aiogram.utils.i18n import I18n, FSMI18nMiddleware

from bot.dispatcher import TOKEN, dp
from bot.handlers.private.book import book_router
from bot.handlers.private.language import lang_router
from bot.handlers.private.order import order_router
from db.models import Base
from db.utils import DB

i18n = I18n(path="locales")

# ngrok http localhost:8080
# WEB_SERVER_HOST = "localhost"
# WEB_SERVER_PORT = 8080
# WEBHOOK_PATH = "/webhook"
# WEBHOOK_SECRET = "my-secret"
# BASE_WEBHOOK_URL = "https://5e07-178-218-201-17.ngrok-free.app"

#
# async def on_startup(bot: Bot) -> None:
#     await bot.set_webhook(f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}", secret_token=WEBHOOK_SECRET)

async def on_startup() -> None:
    dp.include_routers(*[router , book_router , lang_router , order_router])



async def main() -> None:

    dp.startup.register(on_startup)
    dp.update.outer_middleware(FSMI18nMiddleware(i18n))
    bot = Bot(TOKEN)
    Base.metadata.create_all(DB.engine)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

    # app = web.Application()

    # webhook_requests_handler = SimpleRequestHandler(
    #     dispatcher=dp,
    #     bot=bot,
    #     secret_token=WEBHOOK_SECRET,
    # )
    # webhook_requests_handler.register(app, path=WEBHOOK_PATH)
    # setup_application(app, dp, bot=bot)
    # web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())





