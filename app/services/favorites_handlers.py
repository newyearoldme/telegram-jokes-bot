from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from app.parsers.jokes_parser import extract_joke_text
from app.database import crud
from app.keyboards.jokes_keyboard import get_joke_keyboard
from app.keyboards.favorites_keyboard import get_favorite_detail_keyboard
from app.services.display_favorites import show_favorites_list
from app.states.FavoritesState import FavoritesState

async def handle_view_favorite(callback: CallbackQuery, state: FSMContext):
    """Обработка просмотра конкретного анекдота"""
    user_id = callback.from_user.id
    favorite_id = int(callback.data.split("_")[2])

    favorite = await crud.get_favorite_by_id(favorite_id, user_id)
    
    if favorite:
        await state.update_data(current_favorite_id=favorite_id)
        await state.set_state(FavoritesState.viewing_joke)

        await callback.message.edit_text(
            f"{favorite.category}:\n\n{favorite.joke_text}",
            reply_markup=get_favorite_detail_keyboard(favorite_id)
        )
    else:
        await callback.answer("✅ Анекдот уже удалён из избранного")

async def handle_add_favorite(callback: CallbackQuery, state: FSMContext):
    """Обработка добавления в избранное"""
    user_id = callback.from_user.id
    message_text = callback.message.text
    joke_text = extract_joke_text(message_text)
    category = message_text.split("\n\n")[0].replace(":", "").strip()
    
    success = await crud.add_to_favorites(user_id, joke_text, category)
    
    if success:
        data = await state.get_data()
        category_id = data.get("current_category_id")
                
        keyboard = await get_joke_keyboard(category_id, message_text, user_id)
        
        await callback.message.edit_reply_markup(reply_markup=keyboard)
        await callback.answer("✅ Добавлено в избранное!")
    else:
        await callback.answer("❌ Уже в избранном!")

async def handle_confirm_remove(callback: CallbackQuery, state: FSMContext):
    """Обработка подтверждённого удаления"""
    user_id = callback.from_user.id
    data = await state.get_data()
    favorite_id = data.get("remove_favorite_id")
    
    if not favorite_id:
        await callback.answer("❌ Ошибка: ID анекдота не найден")
        await show_favorites_list(callback, state)
        return
    
    success = await crud.delete_favorite(favorite_id, user_id)
    
    if success:
        await show_favorites_list(callback, state)
        await callback.answer("🗑️ Анекдот удалён")
    else:
        await callback.answer("❌ Ошибка удаления")
    
    await state.update_data(remove_favorite_id=None, original_message=None)

async def handle_cancel_remove(callback: CallbackQuery, state: FSMContext):
    """Обработка отмены удаления"""
    data = await state.get_data()
    original_message = data.get("original_message")
    favorite_id = data.get("remove_favorite_id")
    
    if original_message and favorite_id:
        await state.set_state(FavoritesState.viewing_joke)
        await callback.message.edit_text(
            original_message,
            reply_markup=get_favorite_detail_keyboard(favorite_id)
        )
    else:
        await state.set_state(FavoritesState.viewing_list)
        current_page = data.get("current_page", 0)
        await show_favorites_list(callback, state, current_page)
    
    await callback.answer("❌ Удаление отменено")
    await state.update_data(remove_favorite_id=None, original_message=None)
