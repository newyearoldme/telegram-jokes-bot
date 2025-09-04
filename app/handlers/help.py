from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Router

router = Router()

@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
    "Привет! Это бот-анекдотник. Список доступных команд:\n\n" \
    "/joke (/jokes) — показывает анекдот с возможностью выбора категории\n" \
    "/favorites (/favs) — показывает избранные анекдоты\n" \
    )
