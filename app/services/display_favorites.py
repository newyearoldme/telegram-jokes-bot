from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.database import crud
from app.keyboards.favorites_keyboard import get_favorites_pagination_keyboard
from app.states.FavoritesState import FavoritesState

async def show_favorites_list(
    message_or_callback: Message | CallbackQuery,
    state: FSMContext,
    page: int = 0
) -> list | None:
    """Универсальная функция для отображения списка избранного"""
    if isinstance(message_or_callback, Message):
        user_id = message_or_callback.from_user.id
        message = message_or_callback
        is_edit = False
    else:
        user_id = message_or_callback.from_user.id
        message = message_or_callback.message
        is_edit = True
    
    favorites = await crud.get_user_favorites(user_id)
    
    if not favorites:
        text = "📭 У вас нет избранных анекдотов"
        if is_edit:
            await message.edit_text(text)
        else:
            await message.answer(text)
        return None
    
    total_pages = (len(favorites) + 4) // 5
    if page >= total_pages:
        page = total_pages - 1
    
    text = f"📂 Ваши избранные анекдоты ({len(favorites)}):"
    
    if is_edit:
        await message.edit_text(
            text,
            reply_markup=get_favorites_pagination_keyboard(favorites, page)
        )
    else:
        await message.answer(
            text,
            reply_markup=get_favorites_pagination_keyboard(favorites, page)
        )
    
    await state.update_data(favorites=favorites, current_page=page)
    await state.set_state(FavoritesState.viewing_list)
    
    return favorites
