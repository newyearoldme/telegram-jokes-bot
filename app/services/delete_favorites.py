from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from app.parsers.jokes_parser import extract_joke_text
from app.database import crud
from app.keyboards.jokes_keyboard import get_confirmation_keyboard, get_joke_keyboard

async def remove_favorite_with_confirm(callback: CallbackQuery, state: FSMContext):
    """Удаление анекдота с подтверждением"""
    user_id = callback.from_user.id
    message_text = callback.message.text
    joke_text = extract_joke_text(message_text)
    joke_hash = crud.generate_joke_hash(joke_text)

    favorite = await crud.get_favorite_by_hash(user_id, joke_hash)
    if not favorite:
        await callback.answer("✅ Анекдот уже удалён из избранного")
        return

    await state.update_data(
        remove_favorite_id=favorite.id,
        original_message=message_text,
        original_category_id=(await state.get_data()).get("current_category_id")
    )
    
    await callback.message.edit_text(
        f"{message_text}\n\n❓ Вы уверены, что хотите удалить этот анекдот из избранного?",
        reply_markup=get_confirmation_keyboard()
    )
    await callback.answer()

async def remove_favorite_immediate(callback: CallbackQuery, state: FSMContext):
    """Немедленное удаление анекдота (без подтверждения)"""
    user_id = callback.from_user.id
    message_text = callback.message.text
    joke_text = extract_joke_text(message_text)
    joke_hash = crud.generate_joke_hash(joke_text)

    favorite = await crud.get_favorite_by_hash(user_id, joke_hash)
    if not favorite:
        await callback.answer("✅ Анекдот уже удалён из избранного")
        return

    success = await crud.delete_favorite(favorite.id, user_id)
    if success:
        data = await state.get_data()
        category_id = data.get("current_category_id")

        keyboard = await get_joke_keyboard(category_id, message_text, user_id)
        await callback.message.edit_reply_markup(reply_markup=keyboard)
        await callback.answer("🗑️ Удалено из избранного")
    else:
        await callback.answer("❌ Ошибка удаления")
