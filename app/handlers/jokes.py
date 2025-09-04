from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.parsers.jokes_parser import get_random_joke
from app.keyboards.jokes_keyboard import get_category_keyboard, get_joke_keyboard
from app.config import Config

router = Router()

@router.message(Command("joke", "jokes"))
@router.callback_query(F.data == "main_menu")
async def cmd_joke(message_or_callback: Message | CallbackQuery):
    text = "🎭 Выбери категорию анекдотов:"

    if isinstance(message_or_callback, Message):
        await message_or_callback.answer(text, reply_markup=get_category_keyboard())

    else:
        await message_or_callback.message.edit_text(text, reply_markup=get_category_keyboard())
        await message_or_callback.answer()

@router.callback_query(F.data.startswith("category_"))
async def process_category(callback: CallbackQuery, state: FSMContext):
    category_id = callback.data.split("_")[1]
    category_config = Config.categories[category_id]

    joke = await get_random_joke(category_config["url"], category_config["max_pages"])

    await state.update_data(current_category_id=category_id)

    keyboard = await get_joke_keyboard(
        category_id, 
        f"{category_config['name']}:\n\n{joke}",
        callback.from_user.id
    )
    
    await callback.message.edit_text(
        f"{category_config['name']}:\n\n{joke}",
        reply_markup=keyboard
    )
    await callback.answer()
