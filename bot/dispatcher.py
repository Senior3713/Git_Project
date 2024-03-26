from os import getenv
from dotenv import load_dotenv
from aiogram import Dispatcher

load_dotenv('.env')

TOKEN = getenv("BOT_TOKEN")
dp = Dispatcher()