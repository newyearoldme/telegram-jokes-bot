from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import Router

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Привет! Я бот-анекдотник 🤖. Напиши /help чтобы получить список всех доступных команд")
