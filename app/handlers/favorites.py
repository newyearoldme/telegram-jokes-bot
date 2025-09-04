from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from app.services.display_favorites import show_favorites_list
from app.services.delete_favorites import remove_favorite_with_confirm, remove_favorite_immediate
from app.services.favorites_handlers import (
    handle_view_favorite,
    handle_add_favorite, 
    handle_confirm_remove,
    handle_cancel_remove
)

router = Router()

@router.message(Command("favorites", "favorite", "favs", "fav"))
async def show_favorites_handler(message: Message, state: FSMContext):
    await show_favorites_list(message, state)

@router.callback_query(F.data.startswith("fav_page_"))
async def paginate_favorites(callback: CallbackQuery, state: FSMContext):
    page = int(callback.data.split("_")[2])
    await show_favorites_list(callback, state, page)
    await callback.answer()

@router.callback_query(F.data == "fav_list")
async def back_to_list(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    current_page = data.get("current_page", 0)
    await show_favorites_list(callback, state, current_page)
    await callback.answer()

@router.callback_query(F.data.startswith("view_fav_"))
async def view_favorite_detail(callback: CallbackQuery, state: FSMContext):
    await handle_view_favorite(callback, state)
    await callback.answer()

@router.callback_query(F.data == "add_favorite")
async def add_to_favorites_handler(callback: CallbackQuery, state: FSMContext):
    await handle_add_favorite(callback, state)

@router.callback_query(F.data == "remove_favorite")
async def remove_from_favorites_handler(callback: CallbackQuery, state: FSMContext):
    await remove_favorite_immediate(callback, state)

@router.callback_query(F.data.startswith("delete_fav_"))
async def delete_favorite_with_confirm(callback: CallbackQuery, state: FSMContext):
    await remove_favorite_with_confirm(callback, state)

@router.callback_query(F.data == "confirm_remove")
async def confirm_remove_handler(callback: CallbackQuery, state: FSMContext):
    await handle_confirm_remove(callback, state)

@router.callback_query(F.data == "cancel_remove")
async def cancel_remove_handler(callback: CallbackQuery, state: FSMContext):
    await handle_cancel_remove(callback, state)

@router.callback_query(F.data == "no_action")
async def no_action(callback: CallbackQuery):
    await callback.answer()
