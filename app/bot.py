from aiogram import Bot, Dispatcher
from app.config import Config

bot = Bot(token=Config.token)
dp = Dispatcher()
